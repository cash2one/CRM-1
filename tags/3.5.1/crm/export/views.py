# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import codecs
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from utils import format_time
from crm.models import Customer, Project
from crm.customers import filter_customer, query_customer
from crm.projects import filter_project, query_project, sort_by_mark
from accounts.models import UserCredit


class ExportCsv(object):
    """
    export csv
    """
    def __init__(self, filename):
        self.response = HttpResponse(content_type='text/csv')
        self.response.write(codecs.BOM_UTF8)
        self._write_filename(filename)
        self.writer = csv.writer(self.response)

    def _write_filename(self, filename):
        now = datetime.datetime.now()
        self.response['Content-Disposition'] = 'attachment; filename="%s-%s%s%s%s.csv"' \
                                               % (filename, now.year, now.month, now.day, now.microsecond)

    def write_row(self, row):
        row = map(lambda x: unicode(x), row)
        try:
            self.writer.writerow(row)
        except UnicodeEncodeError:
            self.writer.writerow([c.encode('utf-8') for c in row])

    def write_rows(self, rows):
        assert hasattr(rows, '__iter__'), 'rows must be iterable'
        for row in rows:
            self.write_row(row)

    def render_csv_response(self):
        return self.response


class ExportCsvCustomers(ExportCsv):
    """
    export csv customers
    """
    header = (u'客户名称', u'客户简称', u'客户类型', u'客户级别', u'区域', u'注册资本(万)', u'股东', u'客户业务或产品描述',
              u'省份', u'城市', u'地址', u'跟进商务', u'创建时间', u'备注')

    def write_rows(self, customers):
        for c in customers:
            timestamp = format_time(c.timestamp)
            self.write_row([
                c.name,
                c.short_name,
                c.type.name,
                c.get_priority_display(),
                c.zone.name,
                c.registered_capital,
                c.shareholder,
                c.product_desc,
                c.province,
                c.city,
                c.address,
                c.get_businessmans_name(),
                timestamp,
                c.notes])


class ExportCsvProjects(ExportCsv):
    """
    export csv projects
    """
    def write_rows(self, projects, showmark=False):
        for p in projects:
            progress = p.get_cur_progress()
            row = [
                p.name, p.customer.name, p.get_products_name(), p.customer.get_priority_display(),
                p.get_state(), p.get_businessmans_name(), p.get_contacts_name(),
                progress['progress'], progress['desc'], progress['plan'],
                format_time(p.get_latest_progress_updatetime()), format_time(p.timestamp), p.notes
            ]
            if showmark:
                row.append(p.get_mark_content())
            self.write_row(row)


def project_count(projects, progress):
    """根据进度代号判断，统计给定项目中处在该进度期的项目个数"""
    count = 0
    for project in projects:
        if project.get_cur_progress_val() == progress:
            count += 1
    return count


class ExportDataBm(ExportCsv):
    """
    export csv 商务的数据统计
    """
    def write_rows(self, businessmans_table):
        for bm in businessmans_table:
            self.write_row(
                    [bm.user.first_name, bm.customer_set.count(), bm.project_set.count()]+bm.project_count_list()
            )


class ExportDataCustomers(ExportCsv):
    """
    export csv 客户的数据统计
    """
    def write_rows(self, customers):
        for c in customers:
            self.write_row([c.name, c.zone.name, c.type.name, c.project_set.count(), c.get_projects_name()])


@login_required
def export_customers(request):
    """导出客户"""
    typeid = int(request.GET.get('typeid', 0))
    priority = int(request.GET.get('priority', 0))
    zoneid = int(request.GET.get('zoneid', 0))
    time = int(request.GET.get('time', 0))
    customer_name = request.GET.get('customer_name')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    businessman_id = request.GET.get('businessman', 0)  # 商务id, 导出某个商务的客户

    if businessman_id:
        customers = Customer.objects.filter(businessman__id=businessman_id)
    else:
        customers = Customer.objects.all()
    # 过滤
    customers = filter_customer(customers, typeid=typeid, priority=priority, zoneid=zoneid, time=time)
    # 查询
    customers = query_customer(customers, customer_name, date_start, date_end)

    export_csv_customers = ExportCsvCustomers('customers')
    export_csv_customers.write_row(ExportCsvCustomers.header)
    export_csv_customers.write_rows(customers)
    return export_csv_customers.render_csv_response()


def filter_projects_tstate(projects, tstate):
    if tstate == 'nontest':
        # 已申请测试-待测试
        return projects.filter(test_progress=1)
    elif tstate == 'testing':
        # 测试中
        return projects.filter(test_progress=2)
    elif tstate == 'tested':
        # 测试完成
        return projects.filter(tested=True)
    else:
        return projects


def filter_projects_impstate(projects, impstate):
    if impstate == 'noncheckimp':
        # 已申请实施，待审核
        return projects.filter(implement_progress=1)
    elif impstate == 'imp':
        # 审核通过，待实施
        return projects.filter(implement_progress=2)
    elif impstate == 'impdone':
        # 实施完成
        return projects.filter(implement_progress=3)
    else:
        return projects


@login_required
def export_projects(request):
    """导出项目"""
    impstate = request.GET.get('impstate')  # 实施进度
    tstate = request.GET.get('tstate')  # 测试进度
    zoneid = int(request.GET.get('zoneid', 0))
    priority = int(request.GET.get('priority', 0))
    progress = int(request.GET.get('progress', 0))
    productid = int(request.GET.get('productid', 0))
    updatetime = int(request.GET.get('updatetime', 0))
    project_name = request.GET.get('project_name')
    customer_name = request.GET.get('customer_name')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    businessman_id = int(request.GET.get('businessman', 0))  # 商务id, 导出某个商务的项目

    projects = Project.objects.all()
    if businessman_id:
        projects = projects.filter(businessman__id=businessman_id)

    if request.user.usercredit.role.role == u'运营经理':
        projects = projects.filter(products__in=request.user.usercredit.product_set.all())

    if impstate:
        projects = filter_projects_impstate(projects, impstate)

    if tstate:
        # 根据风控经理过滤项目
        projects = projects.filter(testapply__analyser=request.user.usercredit)
        # 根据测试进度过滤
        projects = filter_projects_tstate(projects, tstate)
    # 过滤
    projects = filter_project(projects, zoneid=zoneid, priority=priority, progress=progress,
                              productid=productid, updatetime=updatetime)
    # 查询
    projects = query_project(projects, project_name, customer_name, date_start, date_end)
    export_csv_projects = ExportCsvProjects('projects')
    header = [
        u'项目名称', u'所属客户', u'产品', u'客户级别', u'状态', u'跟进商务',  u'联系人',
        u'最新进度', u'最新进展', u'下一步计划', u'更新时间', u'创建时间', u'备注'
    ]
    # TODO 这里实现的不好, 待优化
    # 如果是高级权限user<flex>导出, 就把mark<标注>字段加上
    privilege = request.user.usercredit.privilege
    showmark = True if privilege > 1 else False
    if showmark:
        header.append(u'标注')
        projects = sort_by_mark(projects)

    export_csv_projects.write_row(header)
    export_csv_projects.write_rows(projects, showmark=showmark)
    return export_csv_projects.render_csv_response()


@login_required
def export_data_businessman(request):
    businessman_id = int(request.GET.get('businessman_id', 0))
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')

    businessmans = UserCredit.objects.filter(role__role=u'商务')
    if request.user.usercredit.role.role == u'商务总监':
        businessmans = businessmans.filter(zone=request.user.usercredit.zone)

    businessmans_table = businessmans
    if businessman_id:
        businessmans_table = businessmans.filter(id=businessman_id).all()

    if start_time and end_time and not businessman_id:
        # 根据时间区间过滤出项目，再从这些项目获得商务人员
        projects = Project.objects.filter(progress__updatetime__gte=start_time).filter(progress__updatetime__lt=end_time)
        businessmans_table = businessmans.filter(project__in=projects.distinct()).all().distinct()

    export_databm = ExportDataBm('data')
    header = (u'商务', u'客户数量', u'项目总量', u'准备期', u'接洽期', u'测试/试用期', u'谈判期', u'上线期', u'售后期')
    export_databm.write_row(header)
    export_databm.write_rows(businessmans_table)
    return export_databm.render_csv_response()


@login_required
def export_data_customer(request):
    customer_name = request.GET.get('c_name', '').strip()
    customer_type_id = int(request.GET.get('c_type', 0))
    date_start = request.GET.get('st', '')
    date_end = request.GET.get('et', '')

    customers = Customer.objects.all()
    if request.user.usercredit.role.role == u'商务总监':
        customers = customers.filter(zone=request.user.usercredit.zone)
    if customer_type_id:
        customers = customers.filter(type__id=customer_type_id)
    if customer_name:
        customers = customers.filter(name__icontains=customer_name)
    if date_start and date_end:
        # 根据时间区间过滤出项目，再获得这些项目的客户
        projects = Project.objects.filter(progress__updatetime__gte=date_start).filter(progress__updatetime__lt=date_end)
        customers = customers.filter(project__in=projects.distinct()).all().distinct()

    export_data_customers = ExportDataCustomers('customers-data')
    header = (u'客户名称', u'所在区域', u'客户类型', u'项目数量', u'项目名称')
    export_data_customers.write_row(header)
    export_data_customers.write_rows(customers)
    return export_data_customers.render_csv_response()

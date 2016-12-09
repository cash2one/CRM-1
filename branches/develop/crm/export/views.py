# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import codecs
import datetime
import logging
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from utils import format_time
from crm.models import Customer, Project , ImpApply
from crm.customers import filter_customer, query_customer
from crm.projects import filter_project, query_project, sort_by_mark
from accounts.models import UserCredit
from crm.common import paginate

ERR_LOG = logging.getLogger('crm_error')

class ExportCsv(object):
    """
    export csv
    """
    def __init__(self, filename):
        self.response = HttpResponse(content_type='text/csv')
        self.response.write(codecs.BOM_UTF8)
        self._write_filename(filename )
        self.writer = csv.writer(self.response )

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
            self.write_row([c.name, c.zone.name, c.type.name, c.project_set.count(), c.get_projects_name() ,c.get_businessmans_name()])


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
        customers = Customer.objects.filter(businessman__id=businessman_id, is_delete=False)
    else:
        customers = Customer.objects.filter(is_delete=False)
    # 过滤
    customers = filter_customer(customers, typeid=typeid, priority=priority, zoneid=zoneid, time=time)
    if request.user.usercredit.role.role == u'商务总监':
        if request.user.usercredit.zone.name != '全国': 
            customers = customers.filter(businessman__zone = request.user.usercredit.zone )
            customers = customers.exclude(businessman__test_flag=True)
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

    projects = Project.objects.filter(is_delete=False)
    if businessman_id:
        projects = projects.filter(businessman__id=businessman_id)

    if request.user.usercredit.role.role == u'运营经理':
        projects = projects.filter(products__in=request.user.usercredit.product_set.all())

    if impstate:
        projects = filter_projects_impstate(projects, impstate)
    if request.user.usercredit.role.role == u'商务总监':
        if request.user.usercredit.zone.name != '全国': 
            projects = projects.filter(businessman__zone = request.user.usercredit.zone )
            projects = projects.exclude(businessman__test_flag=True)

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
        projects = Project.objects.filter(progress__updatetime__gte=start_time, is_delete=False).filter(progress__updatetime__lt=end_time)
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

    customers = Customer.objects.filter(is_delete=False)
    if request.user.usercredit.role.role == u'商务总监':
        customers = customers.filter(zone=request.user.usercredit.zone)
    if customer_type_id:
        customers = customers.filter(type__id=customer_type_id)
    if customer_name:
        customers = customers.filter(name__icontains=customer_name)
    if date_start and date_end:
        # 根据时间区间过滤出项目，再获得这些项目的客户
        projects = Project.objects.filter(progress__updatetime__gte=date_start, is_delete=False).filter(progress__updatetime__lt=date_end)
        customers = customers.filter(project__in=projects.distinct()).all().distinct()

    export_data_customers = ExportDataCustomers('customers-data')
    header = (u'客户名称', u'所在区域', u'客户类型', u'项目数量', u'项目名称', u'跟进商务')
    export_data_customers.write_row(header)
    export_data_customers.write_rows(customers)
    return export_data_customers.render_csv_response()

#################################
# 下载获取交付申请列表数据 start #
#################################
class ExportCsvImpApply(ExportCsv):
    """
    export csv projects
    """
    def write_rows(self, impapply, showmark=False):
        progress_data=dict(ImpApply.PROGRESS_CHOICES)
        pay_type = {'1': '方案一：子产品按量计费','2':'方案二：按授信额比例计费','3':'方案三：风险共担模式','4':'方案四：包年计费'}
        for imp_apply in impapply:
            p=imp_apply.project   
            progress = p.get_cur_progress()
            update_record=''
            extra_fields_mode = ""
            try:
                extra_fields = imp_apply.extra_fields
                for m  in  extra_fields.get("mode"):
                    extra_fields_mode = str(extra_fields_mode + m + ',')
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())  
                

            try:
                description = imp_apply.get_latest_progress().description
                imp_description = ''
                if description != '无' and description != '' :
                    imp_description = imp_apply.get_latest_progress().operator + imp_apply.get_latest_progress().description
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
                imp_description = ''

            if extra_fields.get("account_type") == "2":
                formal = extra_fields.get('pgbg_product').get("formal") 
                cm = extra_fields.get('pgbg_product').get("charge_mode")
            else:
                formal = {}
                cm = {}
            cus = {}
            if  extra_fields.get("cus_config") :
                cus = extra_fields.get("cus_config")

            report_string = u''
            if extra_fields.get("pgbg_product") and extra_fields.get("pgbg_product").get("product_selected").values():
                for p in extra_fields.get("pgbg_product").get("product_selected").values():
                     report_string = report_string + p.get("name") + u'（'+ p.get("code") + u'）'+ u'；' + u'\n' 
                     if p.get("price"):
                        report_string = report_string[:-1]
                        report_string = report_string + u'单价（元）'+ u'：'+ str(p.get("price")) + u'\n' 
            imp_HNApi = u''
            if extra_fields.get("HNApi_selected") and extra_fields.get("HNApi_selected").values():
                for p in extra_fields.get("HNApi_selected").values():
                    note = p.get("note")
                    if isinstance(p.get("note",''),int) :
                            note = str(p.get("note"))
                    if extra_fields.get("account_type") == "1":
                        
                        imp_HNApi =imp_HNApi + p.get("name") +  u'；' + u'测试条数：' + str(p.get("val")) + u'说明：' +  note + u"\n"
                    else:
                        imp_HNApi =imp_HNApi + p.get("name") +  u'；' + u'单价：' + str(p.get("val")) + u'说明：' +  note + u"\n"
            update_record = u''
            if imp_apply.impapplyprogress_set.all():
                for p in imp_apply.impapplyprogress_set.all() :
                       update_record = update_record+p.create_time.strftime("%Y-%m-%d %H:%M:%S") + p.operator + p.description +  progress_data[int(p.progress)] + u"\n"
            try:
                extra_fields = imp_apply.extra_fields
                if extra_fields:
                   counts_type = '测试' if  extra_fields.get("account_type") == '1' else "正式"
                   extra_fields_multi_apply = "是" if extra_fields.get("multi_apply") == "1" else "否"
                   extra_fields_multi_module = "是" if extra_fields.get("multi_module") == "1" else "否"

            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
                extra_fields_multi_apply = ''  
                extra_fields_multi_module = '' 
            test_api_count = u'none'
            test_web_count = u'none'
            if extra_fields.get('account_type') == "1" and  extra_fields.get('pgbg_product') and extra_fields.get('pgbg_product').get('test') :
                test_api_count = extra_fields.get('pgbg_product').get('test').get('api_count')
                test_web_count = extra_fields.get('pgbg_product').get('test').get('web_count')
            ####贷中api上传以及特殊名单上传标记
            apiFileUpload_specialList = ''
            apiFileUpload_dz = ''
            if extra_fields.get("apiFileUpload_specialList",''):
                apiFileUpload_specialList = u'是'
            if extra_fields.get("apiFileUpload_dz",''):
                apiFileUpload_dz = u'是'
            ##七要素
            platform = ''
            web_domain= ''
            app_name = ""
            event = ""
            test_env = u""
            idfa = u""
            ios_lng = u""
            if extra_fields.get("deviceSenvenElement",''):
                element = extra_fields.get("deviceSenvenElement",'')
                test_env = u'是' if element.get("device_anti_fraud_test_env",'') == '1' else u"否"
                idfa = u'是' if element.get("device_anti_fraud_ios_idfa",'') == '1' else u"否"
                ios_lng = u'是' if element.get("device_anti_fraud_ios_lng",'') == '1' else u"否"
                extra_fields = imp_apply.extra_fields
                platform = element.get("device_anti_fraud_platform_web",'')+u";"+\
                element.get("device_anti_fraud_platform_ios",'')+u";"+\
                element.get("device_anti_fraud_platform_android",'')
                web_domain = element.get("device_anti_fraud_platform_web_domin",'')
                app_name = element.get("device_anti_fraud_platform_app_name",'')
                event = element.get("device_anti_fraud_event_borrow_money",'')+u";"+\
                element.get("device_anti_fraud_event_registration",'')+u";"+\
                element.get("device_anti_fraud_event_login",'')

            row = [ 
                imp_apply.id, imp_apply.project.name, imp_apply.project.customer.id, imp_apply.project.customer.name,
                imp_apply.applicant.user.first_name,imp_apply.create_time.strftime("%Y-%m-%d %H:%M:%S"), 
                imp_apply.product.name, imp_apply.analyser.user.first_name, imp_apply.operations.user.first_name,
                imp_apply.imp_engineer.user.first_name, progress_data[int(imp_apply.progress)], imp_description,
                update_record, counts_type,extra_fields.get("date_start"),
                extra_fields.get("target") , extra_fields.get("target_note"), extra_fields_mode, extra_fields_multi_apply,
                extra_fields_multi_module, extra_fields.get("required_key") , test_api_count ,test_web_count,
                formal.get("free_date_start") ,
                formal.get("free_period",'none')+ u"个月", formal.get("free_limit"),formal.get("free_time_note"),
                cm.get("contract_start_date"),cm.get("contract_end_date"),cm.get("basic_service_charge"),
                pay_type.get(cm.get('mode')),cm.get("hit_price"),cm.get("fxgd_note"),cm.get("year_price",'none')+ u"元/" +cm.get("month_price",'none')+ u"月",
                report_string , imp_HNApi ,apiFileUpload_specialList,apiFileUpload_dz,
                cus.get("cus_pf"),cus.get("cus_data"),
                cus.get("rule_blk_sheet"),cus.get("rule_multi_apply"),extra_fields.get("radar_permission"),
                extra_fields.get("notes"),
                imp_apply.contact.name, imp_apply.contact.position, u'`' + imp_apply.contact.tel, imp_apply.contact.mobile,
                imp_apply.contact.email,
                platform,
                web_domain,
                app_name,
                event,
                test_env,
                idfa,
                ios_lng

            ]
            
            if showmark:
                row.append(p.get_mark_content())
            self.write_row(row)




@login_required
def export_impapply_to_csv(request,**kwargs):
    """导出项目"""
    #progress = int(progress)
    usercredit = request.user.usercredit
    project_name = request.GET.get('project_name', '').strip()
    role = usercredit.role.role
    context = {}
    context['product_id'] = int(kwargs.get('product_id', 0))
    context['priority'] = int(kwargs.get('priority', 0))
    
    #context['priority'] = int(kwargs.get('project_name', 0))
    progress = int(kwargs.get('progress', 1))
    page_id = request.GET.get('page', 1)
    imp_apply_list = ImpApply.objects.filter(is_delete = False)
    if progress == 1:
        pass
    elif progress == 2:
        imp_apply_list = imp_apply_list.filter(progress=10)
    elif progress == 3:
        imp_apply_list = imp_apply_list.filter(progress=20)
    elif progress == 4:
        imp_apply_list = imp_apply_list.filter(progress=30)
    elif progress == 5:
        imp_apply_list = imp_apply_list.filter(progress=40)
    elif progress == 6:
        imp_apply_list = imp_apply_list.filter(progress__in=[46,47,48,49])
    elif progress == 7:
        imp_apply_list = imp_apply_list.filter(progress=50)
    elif progress == 8:
        imp_apply_list = imp_apply_list.filter(progress__in=[11, 12, 13])

    
    if role == u'商务':
        imp_apply_list = imp_apply_list.filter(applicant=usercredit)
    elif role == u'风控经理':
        imp_apply_list = imp_apply_list.filter(analyser=usercredit)
    elif role == u'运营经理':
        imp_apply_list = imp_apply_list.filter(operations=usercredit)
    elif role == u'交付经理':
        imp_apply_list = imp_apply_list.filter(imp_engineer=usercredit)
    elif role == u'商务总监':
        imp_apply_list = imp_apply_list.filter(project__customer__zone=usercredit.zone)

    if context['product_id']:
        imp_apply_list = imp_apply_list.filter(product__id=context['product_id'])
    if context['priority']:
        imp_apply_list = imp_apply_list.filter(project__customer__priority=context['priority'])

    export_csv_projects = ExportCsvImpApply('impapply')
    header = [
        u'单号', u'所属项目', u'客户id', u'所属客户',
        u'申请人', u'申请时间', 
        u'产品', u'风控经理', u'运营经理', 
        u'交付经理', u'状态', u'进度描述', 
        u'更新记录', u"账号类型", u"建议对接开始日期",
        u"交付目的", u"补充说明", u"对接形式", u"转正后是否计入多次申请",
        u"分模块调用",u"必填key值", u"API(条/天)", u"网页(总条数)",
        u"免费期开始日期",
        u"免费期限",u"免费查询限额",u"免费期其它说明",
        u"合同开始日期",u"合同截至日期",u"基础服务费(元)",
        u"付费模式",u"每个命中客户的价格",u"风险共担的具体比例",u"包年价格",
        u"交付的评估报告系列产品",u"交付的海纳api产品",u"特殊名单API上传",u"贷中名单API上传",
        u"客制化评分",u"客制化数据",
        u"借款反欺诈规则-黑名单",u"借款反欺诈规则-多次申请",u"雷达平台权限",
        u"附加字段值备注",
        u'联系人', u'职位', u'固话',u'手机',
        u'邮箱' ,
        u'部署平台',
        u'网页域名',
        u'APP名称',
        u'部署事件',
        u'部署测试环境',
        u'IOSAPP是否支持IDFA采集',
        u'IOSAPP是否反馈经纬度'
    ]
    
    if project_name:

        imp_apply_list = imp_apply_list.filter(project__name__contains=project_name)

    # TODO 这里实现的不好, 待优化
    # 如果是高级权限user<flex>导出, 就把mark<标注>字段加上
    privilege = request.user.usercredit.privilege
    showmark = True if privilege > 1 else False
    if showmark:
        header.append(u'标注')
        projects = sort_by_mark(projects)
    #print imp_apply_list[0].id,imp_apply_list[1].id
    data_list = paginate(imp_apply_list, page_id).object_list
    export_csv_projects.write_row(header)
    export_csv_projects.write_rows(data_list, showmark=showmark)
    return export_csv_projects.render_csv_response()
################################
# end                          #
################################

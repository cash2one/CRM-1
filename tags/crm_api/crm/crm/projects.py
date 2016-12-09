# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.generic import View
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import UserCredit, Zone

from .models import Customer, Project, Contact, Progress, Product
from .common import paginate, query_transform, CommonView, TIME_CHOICES, TIMEDT


def filter_project(projects, priority=0, progress=0, productid=0, zoneid=0, updatetime=0):
    """根据客户级别,进度,产品和更新时间筛选项目"""
    if zoneid:
        projects = projects.filter(customer__zone__id=zoneid)
    if priority:
        projects = projects.filter(customer__priority=priority)
    if productid:
        projects = projects.filter(products__id=productid)
    if progress:
         # TODO 通过progress来过滤projects的方法待优化
         # TODO 现在是2016年3月4日优化的, 仍然不合理
        def f(project):
            if project.progress_set.exists():
                return project.progress_set.order_by('updatetime', 'timestamp').last().progress == progress
        project_id_set = [p.id for p in filter(f, projects)]
        projects = projects.filter(id__in=project_id_set)
    if updatetime:
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        period = now - TIMEDT[updatetime]
        projects = projects.filter(progress__updatetime__gte=period)
    return projects.distinct()


def query_project(projects, project_name, customer_name, date_start="", date_end=""):
    if project_name:
        projects = projects.filter(name__icontains=project_name)
    if customer_name:
        projects = projects.filter(Q(customer__name__icontains=customer_name) | Q(customer__short_name__icontains=customer_name))
    if date_start and date_end:
        now = timezone.now()
        date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
        date_start = now.replace(year=date_start.year, month=date_start.month, day=date_start.day,
                                 hour=0, minute=0, second=0, microsecond=0)
        date_end = now.replace(year=date_end.year, month=date_end.month, day=date_end.day,
                               hour=0, minute=0, second=0, microsecond=0)
        date_end = date_end + datetime.timedelta(days=1)
        projects = projects.filter(progress__updatetime__gte=date_start).filter(progress__updatetime__lt=date_end).all()
    return projects.distinct()


def filter_projects_progress(projects, progress):
    """
    根据最新更新的进度(即项目所处的阶段)来过滤项目
    """
    # TODO 此方法只是临时方案
    if not progress:
        return projects

    def f(project):
        if project.progress_set.exists():
            return project.progress_set.latest('updatetime').progress == progress
    return filter(f, projects)


def sort_by_mark(projects):
    """根据mark的更新时间对project排序"""
    tz_base_cmp = timezone.now().replace(1900)

    def keysort(project):
        try:
            return project.progress_set.latest('updatetime').mark.updatetime
        except ObjectDoesNotExist:
            return tz_base_cmp
    return sorted(projects, key=keysort, reverse=True)


class ProjectListBaseView(CommonView):

    def get_context_data(self, **kwargs):
        context = super(ProjectListBaseView, self).get_context_data(**kwargs)
        context['project_priority'] = Customer.PRIORITY_CHOICES
        context['progress_choices'] = Progress.PROGRESS_CHOICES
        context['products'] = Product.objects.all()
        context['time_choices'] = TIME_CHOICES
        context['page_id'] = int(self.request.GET.get('page', 1))
        return context


class Projects(ProjectListBaseView):
    template_name = 'projects.html'
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        context = super(Projects, self).get_context_data(**kwargs)
        context['priority'] = int(kwargs['priority'])
        context['progress'] = int(kwargs['progress'])
        context['productid'] = int(kwargs['productid'])
        context['updatetime'] = int(kwargs['updatetime'])

        context['projects'] = filter_project(
            self.request.user.usercredit.project_set.filter(is_delete=False),
            priority=context['priority'],
            progress=context['progress'],
            productid=context['productid'],
            updatetime=context['updatetime']
        )
        return context

    def get(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        projects = context.pop('projects')
        # 分页
        context['page'] = paginate(projects, context['page_id'])
        # <导出>地址参数
        context['export_url_param'] = query_transform(
            progress=context['progress'],
            priority=context['priority'],
            productid=context['productid'],
            updatetime=context['updatetime'],
            businessman=request.user.usercredit.id
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        # 获取post表单数据
        context['project_name'] = request.POST.get('project-name').strip()
        context['customer_name'] = request.POST.get('customer-name').strip()
        context['date_start'] = request.POST.get('date-start')
        context['date_end'] = request.POST.get('date-end')
        # 根据post表单数据查询
        projects = query_project(
            context.pop('projects'),
            context['project_name'],
            context['customer_name'],
            context['date_start'],
            context['date_end']
        )
        # 分页
        context['page'] = paginate(projects, context['page_id'])
        # <导出>地址参数
        context['export_url_param'] = query_transform(
            progress=context['progress'],
            priority=context['priority'],
            productid=context['productid'],
            updatetime=context['updatetime'],
            businessman=request.user.usercredit.id,
            project_name=context['project_name'],
            customer_name=context['customer_name'],
            date_start=context['date_start'],
            date_end=context['date_end']
        )
        return self.render_to_response(context)


class ProjectList(ProjectListBaseView):
    template_name = 'project-list.html'
    allowed_role = [u'管理层', u'商务总监', u'风控经理']

    def mark_enabled(self):
        """flex的privilege权限设置的是2<高级>, 只针对flex开启标注的功能"""
        privilege = self.request.user.usercredit.privilege
        return privilege > 1

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context.update({'project_name': '', 'customer_name': '', 'date_start': '', 'date_end': ''})
        context['priority'] = int(kwargs['priority'])
        context['progress'] = int(kwargs['progress'])
        context['productid'] = int(kwargs['productid'])
        context['zoneid'] = int(kwargs['zoneid'])
        context['updatetime'] = int(kwargs['updatetime'])
        context['zones'] = Zone.zone_use()

        if self.request.method == 'GET':
            try:
                businessman_id = int(self.request.GET.get('businessman', 0))
            except ValueError:
                raise Http404(u'url参数错误')
        elif self.request.method == 'POST':
            businessman_id = int(self.request.POST.get('businessman-id', 0))
        else:
            raise Http404

        projects = Project.objects.filter(is_delete=False)

        if businessman_id:
            projects = projects.filter(businessman__id=businessman_id)
        businessmans = UserCredit.objects.filter(role__role=u'商务')
        if not self.request.user.usercredit.test_flag:
            businessmans = businessmans.exclude(test_flag=True)
            projects = projects.exclude(businessman__test_flag=True)
        role = self.request.user.usercredit.role.role
        if role == u'商务总监':
            zone = self.request.user.usercredit.zone
            zoneid = zone.id
            
            
            if self.request.user.usercredit.zone.name != u'全国':
                projects = projects.filter(businessman__zone = zone)
                #businessmans = UserCredit.objects.filter(role__role=u'商务')
                businessmans = businessmans.filter(zone__id=zoneid)
                context['zones'] = None
            
            
        # 过滤
        projects = filter_project(
                projects, priority=context['priority'], progress=context['progress'],
                productid=context['productid'], zoneid=context['zoneid'], updatetime=context['updatetime']
        )
        context['businessmans'] = businessmans
        context['businessman_id'] = businessman_id
        context['projects'] = projects
        return context

    def get(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        projects = context.pop('projects')
        # 标注,排序
        showmark = self.mark_enabled()
        if showmark:
            projects = sort_by_mark(projects)
        # 分页
        page = paginate(projects, context['page_id'])

        query_string = query_transform(
                zoneid=context['zoneid'], progress=context['progress'], priority=context['priority'],
                productid=context['productid'], updatetime=context['updatetime'], businessman=context['businessman_id']
        )
        query_string_businessman = query_transform(businessman=context['businessman_id'])
        context.update({
            'page': page,
            'showmark': showmark,
            'query_string_businessman': query_string_businessman,
            'export_url_param': query_string,
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        project_name = request.POST.get('project-name').strip()
        customer_name = request.POST.get('customer-name').strip()
        date_start = request.POST.get('date-start')
        date_end = request.POST.get('date-end')
        # 根据post表单数据查询
        projects = query_project(context.pop('projects'), project_name, customer_name, date_start, date_end)
        # 标注,排序
        showmark = self.mark_enabled()
        if showmark:
            projects = sort_by_mark(projects)
        # 分页
        page = paginate(projects, context['page_id'])
        # <导出>地址参数
        query_string = query_transform(
                zoneid=context['zoneid'], progress=context['progress'], priority=context['priority'],
                productid=context['productid'], updatetime=context['updatetime'], businessman=context['businessman_id'],
                project_name=project_name, customer_name=customer_name, date_start=date_start, date_end=date_end
        )
        query_string_businessman = query_transform(businessman=context['businessman_id'])
        context.update({
            'page': page,
            'project_name': project_name,
            'customer_name': customer_name,
            'date_start': date_start,
            'date_end': date_end,
            'showmark': showmark,
            'query_string_businessman': query_string_businessman,
            'export_url_param': query_string,
        })
        return self.render_to_response(context)


class ProjectListProduct(ProjectListBaseView):

    """运营经理角色的项目列表"""

    template_name = 'project-list-product.html'
    allowed_role = [u'运营经理']

    def get_context_data(self, **kwargs):
        context = super(ProjectListProduct, self).get_context_data(**kwargs)
        context.update({'project_name': '', 'customer_name': '', 'date_start': '', 'date_end': ''})
        context['priority'] = int(kwargs['priority'])
        context['progress'] = int(kwargs['progress'])
        context['productid'] = int(kwargs['productid'])
        context['zoneid'] = int(kwargs['zoneid'])
        context['updatetime'] = int(kwargs['updatetime'])
        context['zones'] = Zone.zone_use()
        # 获取登录用户(运营经理)负责的产品相关的项目
        projects = Project.objects.filter(products__in=self.request.user.usercredit.product_set.all(), is_delete=False)
        # 过滤
        projects = filter_project(
                projects, priority=context['priority'], progress=context['progress'], productid=context['productid'],
                zoneid=context['zoneid'], updatetime=context['updatetime']
        )
        if self.request.method == 'POST':
            # 获取post表单数据
            context['project_name'] = self.request.POST.get('project-name', '').strip()
            context['customer_name'] = self.request.POST.get('customer-name', '').strip()
            context['date_start'] = self.request.POST.get('date-start')
            context['date_end'] = self.request.POST.get('date-end')
            # 根据post表单数据查询
            projects = query_project(
                    projects, context['project_name'], context['customer_name'],
                    context['date_start'], context['date_end']
            )
        # 分页
        page = paginate(projects, context['page_id'])
        # <导出>地址参数
        query_string = query_transform(
                zoneid=context['zoneid'], progress=context['progress'], priority=context['priority'],
                productid=context['productid'], updatetime=context['updatetime'], project_name=context['project_name'],
                customer_name=context['customer_name'], date_start=context['date_start'], date_end=context['date_end']
        )
        context.update({
            'page': page,
            'products': self.request.user.usercredit.product_set.all().order_by('order'),
            'export_url_param': query_string,
        })
        return context


class ProjectListAnalyser(ProjectListBaseView):
    template_name = 'project-list-analyser.html'
    allowed_role = [u'风控经理']

    def filter_projects_tstate(self):
        """根据测试状态过滤项目"""
        tstate = self.kwargs.get('tstate')
        projects = Project.objects.filter(is_delete=False)
        if tstate == 'nontest':  # 已申请测试-待测试
            return projects.filter(test_progress=1)
        elif tstate == 'testing':  # 测试中
            return projects.filter(test_progress=2)
        elif tstate == 'tested':  # 测试完成
            return projects.filter(tested=True)
        else:
            raise Http404(u'url参数错误')

    def get_context_data(self, **kwargs):
        context = super(ProjectListAnalyser, self).get_context_data(**kwargs)
        tstate = kwargs.get('tstate')
        priority = int(kwargs.get('priority'))
        productid = int(kwargs.get('productid'))
        # 获取登录的风控经理所在大区的项目
        # projects = Project.objects.filter(customer__zone=self.request.user.usercredit.zone)
        projects = Project.objects.filter(testapply__analyser=self.request.user.usercredit, is_delete=False)
        # 根据测试状态过滤项目
        projects = self.filter_projects_tstate()
        # 根据风控经理过滤项目
        projects = projects.filter(testapply__analyser=self.request.user.usercredit)
        # 过滤
        projects = filter_project(projects, priority=priority, productid=productid)

        project_name = ''
        customer_name = ''
        if self.request.method == 'POST':
            # 获取post表单数据
            project_name = self.request.POST.get('project-name', '').strip()
            customer_name = self.request.POST.get('customer-name', '').strip()
            # 根据post表单数据查询
            projects = query_project(projects, project_name, customer_name)
        # 分页
        page = paginate(projects, context['page_id'])

        dict_title = {'nontest': u'待测试项目', 'testing': u'测试中项目', 'tested': u'测试完成项目'}
        # <导出>地址参数
        query_string = query_transform(tstate=tstate,
                                       priority=priority,
                                       productid=productid,
                                       project_name=project_name,
                                       customer_name=customer_name)
        c = {
            'page': page,
            'title': dict_title.get(tstate),
            'tstate': tstate,
            'priority': priority,
            'products': Product.objects.all(),
            'productid': productid,
            'project_name': project_name,
            'customer_name': customer_name,
            'export_url_param': query_string,
        }
        return c

    def get(self, request, tstate="", priority=0, productid=0):
        self.check_role()
        context = self.get_context_data()
        return render(request, self.template_name, context)


class ProjectListImp(View):
    template_name = 'project-list-imp.html'

    def check_role(self):
        impstate = self.kwargs.get('impstate')
        role = self.request.user.usercredit.role.role
        if impstate == 'noncheckimp':
            # 只有运营经理才能登录交付审核页面
            if role != u'运营经理':
                raise Http404(u'您无权访问此页！')
        elif impstate == 'imp':
            if role != u'交付经理':
                raise Http404(u'您无权访问此页！')

    def filter_projects_impstate(self, projects):
        impstate = self.kwargs.get('impstate')
        if impstate == 'noncheckimp':
            # 已申请交付，待审核
            return projects.filter(implement_progress=1)
        elif impstate == 'imp':
            # 审核通过，待交付
            return projects.filter(implement_progress=2)
        elif impstate == 'impdone':
            # 交付完成
            return projects.filter(implemented=True)
        else:
            raise Http404(u'url参数错误！')

    def get_context_data(self):
        impstate = self.kwargs.get('impstate')
        priority = int(self.kwargs.get('priority'))
        productid = int(self.kwargs.get('productid'))
        zoneid = int(self.kwargs.get('zoneid'))
        page_id = int(self.kwargs.get('page_id'))

        projects = Project.objects.filter(is_delete=False)
        products = Product.objects.all()
        if self.request.user.usercredit.role.role == u'运营经理':
            # 获取登录用户（运营经理）负责的产品相关的项目
            products = self.request.user.usercredit.product_set.all().order_by('order')
            projects = projects.filter(products__in=products)
        # 根据交付状态过滤项目
        projects = self.filter_projects_impstate(projects)
        # 过滤
        projects = filter_project(projects, priority=priority, productid=productid, zoneid=zoneid)
        project_name = ''
        customer_name = ''
        if self.request.method == 'POST':
            # 获取post表单数据
            project_name = self.request.POST.get('project-name').strip()
            customer_name = self.request.POST.get('customer-name').strip()
            # 根据post表单数据查询
            projects = query_project(projects, project_name, customer_name)
        # 分页
        page = paginate(projects, page_id)

        dict_title = {
            'noncheckimp': u"申请交付项目",
            'imp': u"待交付项目",
            'impdone': u"交付完成项目"
        }
        # <导出>地址参数
        query_string = query_transform(impstate=impstate, priority=priority, productid=productid,
                                       project_name=project_name, customer_name=customer_name)
        c = {
            'page': page,
            'page_id': page_id,
            'title': dict_title.get(impstate),
            'impstate': impstate,
            'project_priority': Project.PRIORITY_CHOICES,
            'priority': priority,
            'products': products,
            'productid': productid,
            'zones': Zone.objects.all()[1:],
            'zoneid': zoneid,
            'project_name': project_name,
            'customer_name': customer_name,
            'export_url_param': query_string,
        }
        return c

    def get(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, impstate="", priority=0, productid=0, zoneid=0, page_id=1):
        self.check_role()
        context = self.get_context_data()
        return render(request, self.template_name, context)


@login_required
def project_add(request):
    context = {
        'customers': request.user.usercredit.customer_set.filter(is_delete=False),
        'products':  Product.objects.all(),
        'progress_choices': Progress.PROGRESS_CHOICES
    }
    return render(request, 'project-add.html', context)


@login_required
@csrf_exempt
@require_POST
def ajax_project_add(request):
    """处理添加项目的ajax请求"""
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError), e:
        return JsonResponse({'msg': unicode(e)})

    project_name = data.get('project_name', '').strip()
    customer_id = data.get('customer_id', 0)
    products_id = data.get('products_id', '').split(',')
    notes = data.get('notes', '').strip()
    contact_list = data.get('contacts', [])

    if Project.objects.filter(name=project_name, is_delete=False).exists():
        return JsonResponse({'msg': '该项目名称已经存在！'})

    contacts = []
    for contact in contact_list:
        contact = Contact.objects.create(
            name=contact[0],
            position=contact[1],
            tel=contact[2],
            mobile=contact[3],
            email=contact[4],
        )
        contacts.append(contact)

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist, e:
        return JsonResponse({'msg': unicode(e)})

    project = Project.objects.create(name=project_name, customer=customer, notes=notes)
    project.businessman.add(request.user.usercredit)
    products = Product.objects.filter(id__in=products_id)
    project.products.add(*products)
    project.contacts.add(*contacts)
    return JsonResponse({'msg': '0'})


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    c = {
        'project': project,
        'products': Product.objects.all(),
        'contacts': project.contacts.all(),
        'progresses': Progress.objects.filter(project=project),
        'progress_choices': Progress.PROGRESS_CHOICES
    }
    return render(request, 'project-edit.html', c)


@login_required
def ajax_project_edit(request):
    project_id = request.GET.get('project_id', 0)
    project_name = request.GET.get('project_name', '')
    customer_id = request.GET.get('customer_id', 0)
    products_id = request.GET.get('products_id', '').split(',')
    notes = request.GET.get('notes', '')
    businessmans_id = request.GET.get('businessmans_id', '').split(',')
    try:
        project = Project.objects.get(id=project_id, is_delete=False)
    except Project.DoesNotExist, e:
        return JsonResponse({'msg': unicode(e)})

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist, e:
        return JsonResponse({'msg': unicode(e)})

    businessmans = UserCredit.objects.filter(id__in=businessmans_id)
    products = Product.objects.filter(id__in=products_id)
    project.name = project_name
    project.customer = customer
    project.notes = notes
    project.save()
    project.businessman.clear()
    project.businessman.add(*businessmans)
    project.products.clear()
    project.products.add(*products)
    return JsonResponse({'msg': '0'})


@login_required
def ajax_project_del(request):
    project_id = request.GET.get('project_id', 0)
    try:
        project = Project.objects.get(id=project_id, is_delete=False)
    except Project.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    imps = project.impapply_set.all()
    for imp in imps:
        imp.is_delete = True
        imp.save()
    tests = project.testapply_set.all()
    for test in tests:
        test.is_delete = True
        test.save()
    pros = project.progress_set.all()
    for pro in pros:
        pro.is_delete = True
    contacts = project.contacts.all()
    for contact in contacts:
        contact.is_delete = True
        contact.save()
    project.is_delete = True
    project.save()
    return JsonResponse({'msg': '0'})


@login_required
def project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progresses = Progress.objects.filter(project=project)
    c = {
        'project': project,
        'contacts': project.contacts.all(),
        'progresses': progresses,
    }
    return render(request, 'project-view.html', c)


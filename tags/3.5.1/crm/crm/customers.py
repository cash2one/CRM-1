# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q

from accounts.models import UserCredit, Zone
from utils import format_time

from .models import Customer, CustomerType, CustomerCategory1, CustomerCategory2, CustomerCategory3
from .common import (
    paginate, query_transform, CommonView, PROVINCES, TIME_CHOICES, TIMEDT
)


def common_data(request):
    """ 获取一些渲染客户页面的通常都能用到的数据 """
    # 获取登录用户的所有客户
    customers = request.user.usercredit.customer_set.all()
    # 获取所有的客户类型
    customer_type = CustomerType.objects.all()
    # 获取该大区内所有商务
    zone_businessman = request.user.usercredit.zone.usercredit_set.filter(role__role=u'商务').all()
    if not request.user.usercredit.test_flag:
        # 过滤掉测试账号
        zone_businessman = zone_businessman.exclude(test_flag=True)
    c = {
        'customers': customers,
        'customer_type': customer_type,
        'customer_priority': Customer.PRIORITY_CHOICES,
        'provinces': PROVINCES,
        'zones': Zone.zone_use(),
        'zone_businessman': zone_businessman,
    }
    return c


def filter_customer(customers, typeid=0, priority=0, zoneid=0, time=0):
    """ 根据客户类型,客户级别,时间区间筛选客户 """
    if typeid:
        customers = customers.filter(type__id=typeid)
    if priority:
        customers = customers.filter(priority=priority)
    if zoneid:
        customers = customers.filter(zone__id=zoneid)
    if time:
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        period = now - TIMEDT[time]
        customers = customers.filter(timestamp__gte=period)
    return customers


def query_customer(customers, customer_name, date_start, date_end):
    """根据表单数据查询Customer"""
    if customer_name:
        customers = customers.filter(Q(name__icontains=customer_name) | Q(short_name__icontains=customer_name))
    if date_start and date_end:
        now = timezone.now()
        date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
        date_start = now.replace(year=date_start.year, month=date_start.month, day=date_start.day,
                                 hour=0, minute=0, second=0, microsecond=0)
        date_end = now.replace(year=date_end.year, month=date_end.month, day=date_end.day,
                               hour=0, minute=0, second=0, microsecond=0)
        date_end = date_end + datetime.timedelta(days=1)
        customers = customers.filter(timestamp__gte=date_start).filter(timestamp__lt=date_end).all()
    return customers


class CustomerBaseView(CommonView):

    def get_context_data(self, **kwargs):
        context = super(CustomerBaseView, self).get_context_data(**kwargs)
        context.update({
            'customer_type': CustomerType.objects.all(),
            'customer_priority': Customer.PRIORITY_CHOICES,
            'time_choices': TIME_CHOICES,
        })
        return context


class CustomersMine(CustomerBaseView):
    template_name = 'customers-mine.html'
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        businessman = self.request.user.usercredit
        customers = businessman.customer_set.all()
        typeid = int(kwargs['typeid'])
        priority = int(kwargs['priority'])
        time = int(kwargs['time'])
        page_id = int(self.request.GET.get('page', 1))
        # 筛选
        customers = filter_customer(customers, typeid=typeid, priority=priority, time=time)
        customer_name = date_start = date_end = ''
        if self.request.method == 'POST':
            # 获取post值
            customer_name = self.request.POST.get('customer-name').strip()
            date_start = self.request.POST.get('date-start')
            date_end = self.request.POST.get('date-end')
            # 查询
            customers = query_customer(customers, customer_name, date_start, date_end)
        # 分页
        page = paginate(customers, current_page=page_id)
        # 导出地址参数
        query_string = query_transform(typeid=typeid, priority=priority, time=time, businessman=businessman.id,
                                       customer_name=customer_name, date_start=date_start, date_end=date_end)
        context = super(CustomersMine, self).get_context_data(**kwargs)
        context.update({
            'page': page,
            'page_id': page_id,
            'typeid': typeid,
            'priority': priority,
            'time': time,
            'customer_name': customer_name,
            'date_start': date_start,
            'date_end': date_end,
            'export_url_param': query_string,
        })
        return context


class CustomersAll(CustomerBaseView):
    template_name = 'customers-all.html'
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        # 过滤掉测试账号创建的客户
        if not self.request.user.usercredit.test_flag:
            customers = customers.exclude(businessman__test_flag=True)
        typeid = int(kwargs['typeid'])
        priority = int(kwargs['priority'])
        zoneid = int(kwargs['zoneid'])
        time = int(kwargs['time'])
        page_id = int(self.request.GET.get('page', 1))
        # 筛选
        customers = filter_customer(customers, typeid=typeid, priority=priority, zoneid=zoneid, time=time)
        customer_name = date_start = date_end = ''
        if self.request.method == 'POST':
            # 获取post值
            customer_name = self.request.POST.get('customer-name').strip()
            date_start = self.request.POST.get('date-start')
            date_end = self.request.POST.get('date-end')
            # 查询
            customers = query_customer(customers, customer_name, date_start, date_end)
        # 分页
        page = paginate(customers.distinct(), current_page=page_id)
        # 导出地址参数
        query_string = query_transform(typeid=typeid, priority=priority, time=time, zoneid=zoneid,
                                       customer_name=customer_name, date_start=date_start, date_end=date_end)
        context = super(CustomersAll, self).get_context_data(**kwargs)
        context.update({
            'page': page,
            'page_id': page_id,
            'typeid': typeid,
            'priority': priority,
            'zones': Zone.zone_use(),
            'zoneid': zoneid,
            'time': time,
            'customer_name': customer_name,
            'date_start': date_start,
            'date_end': date_end,
            'export_url_param': query_string,
        })
        return context


class CustomerList(CustomersAll):
    template_name = 'customer-list.html'
    allowed_role = [u'管理层', u'商务总监', u'运营经理', u'风控经理']


class CustomerAdd(CustomerBaseView):
    template_name = 'customer-add.html'
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        context = super(CustomerAdd, self).get_context_data(**kwargs)
        context['customers'] = self.request.user.usercredit.customer_set.all()
        context['provinces'] = PROVINCES
        context['zones'] = Zone.zone_use()
        zone_businessman = self.request.user.usercredit.zone.usercredit_set.filter(role__role=u'商务').all()
        if not self.request.user.usercredit.test_flag:
            zone_businessman = zone_businessman.filter(test_flag=False).all()
        context['zone_businessman'] = zone_businessman
        return context


@csrf_exempt
@login_required
def ajax_customer_add(request):
    """处理添加客户的ajax请求,完成客户的添加"""
    try:
        data = json.loads(request.body)  # 从ajax-post请求中获取数据
    except (ValueError, TypeError), e:
        return JsonResponse({'msg': unicode(e)})
    try:
        customer_name = data.get('name', '').strip()
        customer_short_name = data.get('short_name', '').strip()
        customer_type_id = data.get('type', '').strip()
        category1_id = int(data.get('category1', 0))
        category2_id = int(data.get('category2', 0))
        category3_id = int(data.get('category3', 0))
        customer_priority = int(data.get('priority', 2))
        customer_zone_id = int(data.get('zone', 1))
        registered_capital = int(data.get('registered_capital', 1))
        shareholder = data.get('shareholder', '').strip()
        product_desc = data.get('product_desc', '').strip()
        province = data.get('province', '').strip()
        city = data.get('city', '').strip()
        address = data.get('address', '').strip()
        businessmans_id = data.get('businessmans_id')
        notes = data.get('notes', '').strip()
        # 验证必填项是否有为空的
        if not all((customer_name, customer_short_name, city, registered_capital, shareholder, product_desc)):
            return JsonResponse({'msg': u'有必填项为空'})
        # 判断客户名是否存在
        if Customer.objects.filter(name=customer_name).exists():
            return JsonResponse({'msg': u'该客户已经存在--%s' % customer_name})
        # 大区
        zone = request.user.usercredit.zone
        if zone.name == u'全国':
            zone = Zone.objects.get(id=customer_zone_id)
        category1 = None
        category2 = None
        category3 = None
        if category1_id:
            category1 = CustomerCategory1.objects.get(id=category1_id)
        if category2_id:
            category2 = CustomerCategory2.objects.get(id=category2_id)
        if category3_id:
            category3 = CustomerCategory3.objects.get(id=category3_id)
        # 获取客户类型实例
        customer_type = CustomerType.objects.get(id=customer_type_id)
        # 获取选中的商务人员实例
        businessmans = UserCredit.objects.filter(id__in=businessmans_id).all()
        # 创建客户实例
        customer = Customer.objects.create(
            name=customer_name, short_name=customer_short_name, type=customer_type, priority=customer_priority,
            zone=zone, registered_capital=registered_capital, shareholder=shareholder,
            product_desc=product_desc, province=province, city=city, address=address, notes=notes,
            category1=category1, category2=category2, category3=category3
        )
        # 关联客户和商务的manytomany关系
        customer.businessman.add(*businessmans)
        return JsonResponse({'msg': '0'})
    except Exception:
        import traceback
        traceback.print_exc()


@login_required
def customer_edit(request, pk):
    """根据请求的客户id返回该客户的编辑页面"""
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        raise Http404(u'客户不存在')
    c = common_data(request)
    c['customer'] = customer
    c['customer_businessman_set'] = customer.businessman.all()
    c['category1_set'] = CustomerCategory1.objects.all()
    c['category2_set'] = CustomerCategory2.objects.filter(category1=customer.category1).all()
    c['category3_set'] = CustomerCategory3.objects.filter(category2=customer.category2).all()
    return render(request, 'customer-edit.html', c)


@csrf_exempt
@login_required
def ajax_customer_edit(request):
    """处理客户编辑的ajax请求,完成客户信息的更新"""
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError) as e:
        return JsonResponse({'msg': unicode(e)})
    customer_id = int(data.get('id', 0))
    customer_name = data.get('name', '').strip()
    customer_short_name = data.get('short_name', '').strip()
    customer_type_id = data.get('type', '').strip()
    category1_id = int(data.get('category1', 0))
    category2_id = int(data.get('category2', 0))
    category3_id = int(data.get('category3', 0))
    customer_priority = int(data.get('priority', 2))
    customer_zone_id = int(data.get('zone', 1))
    registered_capital = int(data.get('registered_capital', 0))
    shareholder = data.get('shareholder', '').strip()
    product_desc = data.get('product_desc', '').strip()
    province = data.get('province', '').strip()
    city = data.get('city', '').strip()
    address = data.get('address', '').strip()
    businessmans_id = data.get('businessmans_id', [])
    notes = data.get('notes', '').strip()
    # 验证必填项是否有为空的
    if not all([customer_name, customer_short_name, city, registered_capital, shareholder, product_desc]):
        return JsonResponse({'msg': u'有必填项为空'})
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    # 更新信息
    customer.name = customer_name
    customer.short_name = customer_short_name
    customer.type = CustomerType.objects.get(id=customer_type_id)
    customer.category1 = CustomerCategory1.objects.get(id=category1_id) if category1_id else None
    customer.category2 = CustomerCategory2.objects.get(id=category2_id) if category2_id else None
    customer.category3 = CustomerCategory3.objects.get(id=category3_id) if category3_id else None
    customer.priority = customer_priority
    zone = request.user.usercredit.zone
    customer.zone = zone if zone.name != u'全国' else Zone.objects.get(id=customer_zone_id)
    customer.registered_capital = registered_capital
    customer.shareholder = shareholder
    customer.product_desc = product_desc
    customer.province = province
    customer.city = city
    customer.address = address
    customer.notes = notes
    customer.save(force_update=True)
    customer.businessman.clear()
    # 获取选中的商务人员实例
    businessmans = UserCredit.objects.filter(id__in=businessmans_id)
    # 关联客户和商务的manytomany关系
    customer.businessman.add(*businessmans)
    return JsonResponse({'msg': '0'})


@login_required
def customer_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer-view.html', {'customer': customer})


@login_required
def ajax_customer_view(request):
    """查看客户"""
    customer_id = request.GET.get('customer_id', 0)
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'msg': u'客户不存在'})
    msg = {
        'msg': '0',
        'data': [
            {'name': u'客户id', 'value': customer.id},
            {'name': u'全称', 'value': customer.name},
            {'name': u'简称', 'value': customer.short_name},
            {'name': u'类型', 'value': customer.type.name},
            {'name': u'一级类目', 'value': customer.category1.name if customer.category1 else ''},
            {'name': u'二级类目', 'value': customer.category2.name if customer.category2 else ''},
            {'name': u'三级类目', 'value': customer.category3.name if customer.category3 else ''},
            {'name': u'客户级别', 'value': customer.get_priority_display()},
            {'name': u'区域', 'value': customer.zone.name},
            {'name': u'注册资本', 'value': customer.registered_capital},
            {'name': u'股东', 'value': customer.shareholder},
            {'name': u'客户业务或产品描述', 'value': customer.product_desc},
            {'name': u'省份', 'value': customer.province},
            {'name': u'城市', 'value': customer.city},
            {'name': u'详细地址', 'value': customer.address},
            {'name': u'跟进商务', 'value': customer.get_businessmans_name()},
            {'name': u'备注', 'value': customer.notes},
            {'name': u'创建时间', 'value': format_time(customer.timestamp)},
        ],
    }
    return JsonResponse(msg)


@login_required
def ajax_customer_del(request):
    """删除客户"""
    customer_id = request.GET.get('customer_id', 0)
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'msg': u'客户不存在'})
    # 该客户下的项目也一起删除
    customer_projects = customer.project_set.all()
    customer_projects.delete()
    customer.delete()
    return JsonResponse({'msg': '0'})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import datetime
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserCredit

from .models import Customer, CustomerType, Project, Contact, Progress, Mark
from .common import paginate, query_transform, CommonView


ERRLOG = logging.getLogger('crm_error')


#################################################################
#                         标注相关操作
#################################################################

@login_required
@csrf_exempt
@require_POST
def ajax_mark_edit(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError) as e:
        return JsonResponse({'msg': unicode(e)})

    progress_id = data.get('progress_id', 0)
    content = data.get('content', '').strip()
    marks = Mark.objects.filter(progress__id=progress_id)
    if marks.exists():
        marks.update(content=content, updatetime=datetime.datetime.now())
    else:
        Mark.objects.create(
            usercredit=request.user.usercredit,
            progress=Progress.objects.get(id=progress_id),
            content=content,
            updatetime=datetime.datetime.now()
        )
    return JsonResponse({'msg': '0'})



#################################################################
#                         进度相关操作
#################################################################

@login_required
@csrf_exempt
@require_POST
def ajax_progress_add(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError) as e:
        return JsonResponse({'msg': unicode(e)})

    project_id = data.get('project_id', 0)
    progress_int = data.get('progress', 0)
    description = data.get('description', '').strip()
    plan = data.get('plan', '').strip()
    updatetime = data.get('updatetime', '').strip()
    if not updatetime:
        updatetime = datetime.date.today()

    try:
        project = Project.objects.get(id=project_id, is_delete=False)
    except Project.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})

    role = request.user.usercredit.role.role
    if role == u'风控经理':
        test_progress_int = int(data.get('test_progress', 0))
        project.test_progress = test_progress_int
        if test_progress_int == 3:  # 测试完成
            project.tested = True
            test_apply = project.testapply_set.latest('timestamp')
            test_apply.state = True  # 将测试申请标记为--已测试
            test_apply.save()
    if role == u'交付经理':
        imp_progress_int = int(data.get('imp_progress', 0))
        project.implement_progress = imp_progress_int
        if imp_progress_int == 3:  # 交付完成
            project.implemented = True
            imp_apply = project.impapply_set.latest('timestamp')
            imp_apply.state = True  # 将交付申请标记为--已交付
            imp_apply.save()
    project.save()

    # TODO 此处运营经理更新的进度暂时标记为商务了,如无功能性必要可以不改
    ptype = {u'商务': 0, u'风控经理': 1, u'交付经理': 2, u'运营经理': 0}
    Progress.objects.create(ptype=ptype.get(role), project=project, progress=progress_int,
                            description=description, plan=plan, updatetime=updatetime,
                            operator=request.user.first_name)
    return JsonResponse({'msg': 0})


@login_required
@csrf_exempt
@require_POST
def ajax_progress_edit(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError) as e:
        return JsonResponse({'msg': unicode(e)})
    progress_id = data.get('progress_id', 0)
    progress_int = data.get('progress', 0)
    description = data.get('description', '').strip()
    plan = data.get('plan', '').strip()
    updatetime = data.get('updatetime', '').strip()
    if not updatetime:
        updatetime = datetime.date.today()
    Progress.objects.filter(id=progress_id).update(progress=progress_int, description=description,
                                                   plan=plan, updatetime=updatetime)
    return JsonResponse({'msg': 0})


@login_required
def ajax_progress_del(request):
    progress_id = request.GET.get('progress_id', 0)
    try:
        progress = Progress.objects.get(id=progress_id)
    except Progress.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    progress.delete()
    return JsonResponse({'msg': 0})


#################################################################
#                         联系人相关操作
#################################################################

@login_required
def ajax_contact_add(request):
    project_id = request.GET.get('project_id', 0)
    name = request.GET.get('name', '')
    pos = request.GET.get('pos', '')
    tel = request.GET.get('tel', '')
    mobile = request.GET.get('mobile', '')
    mail = request.GET.get('mail', '')
    if not all([name, mobile, mail]):
        return JsonResponse({'msg': u'名字，手机和邮箱不能为空！'})
    try:
        project = Project.objects.get(id=project_id, is_delete=False)
    except Project.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    contact = Contact.objects.create(name=name, position=pos, tel=tel, mobile=mobile, email=mail)
    project.contacts.add(contact)
    return JsonResponse({'msg': 0, 'contact_id': contact.id, 'contact_name': contact.name})


@login_required
def ajax_contact_view(request):
    contact_id = request.GET.get('contact_id', 0)
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return JsonResponse({'msg': u'联系人不存在!'})
    return JsonResponse({
            'msg': 0,
            'name': contact.name,
            'pos': contact.position,
            'phone': contact.tel,
            'mobile': contact.mobile,
            'mail': contact.email,
    })


@login_required
def ajax_contact_edit(request):
    contact_id = request.GET.get('contact_id', 0)
    name = request.GET.get('name', '')
    pos = request.GET.get('pos', '')
    tel = request.GET.get('tel', '')
    mobile = request.GET.get('mobile', '')
    mail = request.GET.get('mail', '')
    if not all([name, mobile, mail]):
        return JsonResponse({'msg': u'名字，手机和邮箱不能为空！'})
    Contact.objects.filter(id=contact_id).update(name=name, position=pos, tel=tel, mobile=mobile, email=mail)
    return JsonResponse({'msg': 0})


@login_required
def ajax_contact_del(request):
    contact_id = request.GET.get('contact_id', 0)
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    if contact.testapply_set.exists():
        return JsonResponse({'msg': '有测试申请用到这个联系人！'})
    if contact.impapply_set.exists():
        return JsonResponse({'msg': '有交付申请用到这个联系人！'})
    contact.delete()
    return JsonResponse({'msg': 0})


#################################################################
#                          数据统计
#################################################################

class DataBm(CommonView):
    template_name = 'data-businessman.html'
    allowed_role = [u'管理层', u'商务总监']

    def get_context_data(self, **kwargs):
        businessmans = UserCredit.objects.filter(role__role=u'商务')
        if not self.request.user.usercredit.test_flag:
            businessmans = businessmans.filter(test_flag=False)
        if self.request.user.usercredit.role.role == u'商务总监':
            businessmans = businessmans.filter(zone=self.request.user.usercredit.zone)

        businessman_id = int(self.request.POST.get('businessman-id', 0))
        start_time = self.request.POST.get('start-time', '')
        end_time = self.request.POST.get('end-time', '')

        businessmans_table = businessmans
        if businessman_id:
            businessmans_table = businessmans.filter(id=businessman_id).all()

        if start_time and end_time and not businessman_id:
            # 根据时间区间过滤出项目，再从这些项目获得商务人员
            projects = Project.objects.filter(progress__updatetime__gte=start_time).filter(progress__updatetime__lt=end_time, is_delete=False)
            businessmans_table = businessmans.filter(project__in=projects.distinct()).all().distinct()

        # <导出>地址参数
        query_string = query_transform(businessman_id=businessman_id, start_time=start_time, end_time=end_time)

        c = {
            'businessmans': businessmans,  # 下拉选择框里要显示的商务
            'businessman_select': businessman_id,
            'businessmans_table': businessmans_table,  # 统计表格里要显示的商务
            'start_time': start_time,
            'end_time': end_time,
            'export_url_param': query_string
        }
        return c


class DataCustomer(CommonView):
    template_name = 'data-customer.html'
    allowed_role = [u'管理层', u'商务总监']

    def get_context_data(self, **kwargs):
        customer_name = self.request.GET.get('c_name', '').strip()
        customer_type_id = int(self.request.GET.get('c_type', 0))
        start_time = self.request.GET.get('st', '')
        end_time = self.request.GET.get('et', '')

        if self.request.method == 'POST':
            customer_name = self.request.POST.get('customer-name', '').strip()
            customer_type_id = int(self.request.POST.get('customer-type', 0))
            start_time = self.request.POST.get('start-time', '')
            end_time = self.request.POST.get('end-time', '')

        customers = Customer.objects.filter(is_delete=False).all()
        if not self.request.user.usercredit.test_flag:
            customers = customers.filter(businessman__test_flag=False)
        if self.request.user.usercredit.role.role == u'商务总监':
            customers = customers.filter(zone=self.request.user.usercredit.zone)
        if customer_type_id:
            customers = customers.filter(type__id=customer_type_id)
        if customer_name:
            customers = customers.filter(name__icontains=customer_name)
        if start_time and end_time:
            # 根据时间区间过滤出项目，再获得这些项目的客户
            projects = Project.objects.filter(progress__updatetime__gte=start_time, is_delete=False).filter(progress__updatetime__lt=end_time)
            customers = customers.filter(project__in=projects.distinct()).all().distinct()
        # 地址参数
        query_string = query_transform(c_name=customer_name, c_type=customer_type_id, st=start_time, et=end_time)
        # 分页
        page_id = int(self.request.GET.get('page', 1))
        page = paginate(customers, current_page=page_id, page_num=50)
        c = {
            'page': page,
            'customer_name': customer_name,
            'type_select': customer_type_id,
            'customer_type': CustomerType.objects.all(),
            'start_time': start_time,
            'end_time': end_time,
            'export_url_param': query_string
        }
        return c


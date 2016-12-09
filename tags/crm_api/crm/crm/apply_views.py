# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import copy
import traceback
import logging
import time 

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q

from accounts.models import UserCredit
from i_bankserver.models import BProduct
from utils import post_dts, email_validate

from .email_alert import (
    email_alert, test_apply_refuse_email_alert, imp_apply_refuse_email_alert, imp_apply_done_email_alert,
    send_to_impapply_email ,turn_to_applicant_email ,return_to_applicant_email,send_to_test_email
)
from .common import CommonView, paginate, query_transform
from .models import (
    Project, Product, TestResult, TestApply, ImpApply, Config, Customer,
    Contact, TestApplyProgress, ImpApplyProgress, HNApiProduct, JsonConfig
)

ERR_LOG = logging.getLogger('crm_error')

class TestApplyListView(CommonView):
    template_name = 'test-apply-list.html'
    allowed_role = [u'风控经理', u'商务', u'商务总监', u'管理层']

    def get_context_data(self, **kwargs):
        context = super(TestApplyListView, self).get_context_data(**kwargs)
        context['product_id'] = int(kwargs.get('product_id', 0))
        context['priority'] = int(kwargs.get('priority', 0))
        context['progress'] = int(kwargs.get('progress', 1))
        context['page_id'] = int(self.request.GET.get('page', 1))
        context['progress_choices'] = TestApply.PROGRESS_CHOICES
        context['customer_priority'] = Customer.PRIORITY_CHOICES
        context['products'] = Product.objects.all()
        usercredit = self.request.user.usercredit
        test_apply_list = TestApply.objects.filter(is_delete=False)
        if usercredit.role.role == u'风控经理':
            test_apply_list = test_apply_list.filter(analyser=usercredit)
        elif usercredit.role.role == u'商务':
            test_apply_list = test_apply_list.filter(applyman=usercredit)
        elif usercredit.role.role == u'商务总监':
            test_apply_list = test_apply_list.filter(project__customer__zone=usercredit.zone)
        # if not usercredit.test_flag:
        #     test_apply_list = test_apply_list.exclude(applyman__test_flag=True)
        test_apply_list = test_apply_list.filter(progress=context['progress'])
        if context['priority']:
            test_apply_list = test_apply_list.filter(project__customer__priority=context['priority'])
        if context['product_id']:
            test_apply_list = test_apply_list.filter(project__products__id__in=[context['product_id']])
        context['test_apply_list'] = test_apply_list
        return context

    def get(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        test_apply_list = context.pop('test_apply_list')
        project_name = request.GET.get('project_name', '').strip()
        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            test_apply_list = test_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(test_apply_list, context['page_id'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        test_apply_list = context.pop('test_apply_list')
        project_name = request.POST.get('project_name', '').strip()
        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            test_apply_list = test_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(test_apply_list, context['page_id'])
        return self.render_to_response(context)


class TestApplyAddView(CommonView):
    template_name = "test-apply-add.html"
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        context = super(TestApplyAddView, self).get_context_data(**kwargs)
        analysers = UserCredit.objects.filter(role__role=u'风控经理').all()
        if not self.request.user.usercredit.test_flag:
            analysers = analysers.filter(test_flag=False)
        context.update({
            'project': get_object_or_404(Project, id=self.args[0]),
            'analysers': analysers,
            'test_result': TestResult.objects.all()
        })
        return context


class TestApplyEditView(CommonView):
    template_name = "test-apply-edit.html"
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        context = super(TestApplyEditView, self).get_context_data(**kwargs)
        analysers = UserCredit.objects.filter(role__role=u'风控经理').all()
        if not self.request.user.usercredit.test_flag:
            analysers = analysers.filter(test_flag=False)
        context.update({
            'test_apply': get_object_or_404(TestApply, id=self.args[0]),
            'analysers': analysers,
            'test_result': TestResult.objects.all()
        })
        return context


@csrf_exempt
@login_required
def ajax_test_apply_add(request):
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        analyser_id = data.get('analyser_id')
        amount_data = data.get('amount_data', 0)
        goal = data.get('goal').strip()
        fields = data.get('fields').strip()
        overdue_state = data.get('overdue_state', False)
        notes = data.get('notes').strip()
        test_result_selected = data.get('test_result_id', [])  # 选中的测试结果要求
        contact_id = data.get('contact_id')
        try:
            project = Project.objects.get(id=project_id, is_delete=False)
        except Project.DoesNotExist as e:
            return JsonResponse({'msg': unicode(e)})
        analyser = UserCredit.objects.get(id=analyser_id)
        contact = Contact.objects.get(id=contact_id)
        contact_email = contact.email
        if not contact_email or not email_validate(contact_email):
            return JsonResponse({'msg': '选中联系人的email地址有误'})

        dts_account = 'demo%s' % project_id  # 生成dts账号
        test_apply = TestApply(
                applyman=request.user.usercredit, project=project, dts_account=dts_account,
                analyser=analyser, amount_data=amount_data, goal=goal, test_fields=fields,
                overdue_state=overdue_state, contact=contact, notes=notes
        )
        if not TestApply.objects.filter(project=project, is_delete=False).exists():
            # 给DTS发送开账号的数据
            dts_url = Config.objects.filter(name='dts_url').first().value
            if not dts_url:
                return JsonResponse({'msg': '没有获取到DTS的接口地址'})
            try:
                post_dts(dts_url, login_name=dts_account, user_name=project.customer.name, city=project.customer.city,
                         email=contact_email, analy=analyser.user.first_name)
            except ValueError as e:
                ERR_LOG.error(traceback.format_exc())
                return JsonResponse({'msg': unicode(e)})
            except Exception as e:
                ERR_LOG.error(traceback.format_exc())
                return JsonResponse({'msg': '向DTS传输开户数据时出错:%s' % e})
        # 先发邮件提醒和post dts 如果没问题,在存储测试申请进数据库
        test_apply.save()
        # 添加测试结果要求的manytomany关系
        for test_result_id in test_result_selected:
            test_apply.test_result.add(TestResult.objects.get(id=test_result_id))
        # 发邮件提醒给风控经理
        try:
            #email_alert([analyser.user.email], alert=1)
            send_to_test_email([analyser.user.email],test_apply.id , email_type = u'测试申请')
        except Exception as e:
            ERR_LOG.error(traceback.format_exc())
            return JsonResponse({'msg': u'向风控经理发送邮件失败:%s; 请自行通知相关风控经理处理！' % e})
        return JsonResponse({'msg': 0})
    except Exception:
        traceback.print_exc()
        ERR_LOG.error(traceback.format_exc())

@csrf_exempt
@login_required
def ajax_test_apply_edit(request):
    data = json.loads(request.body)
    test_apply_id = data.get('test_apply_id', 0)
    analyser_id = data.get('analyser_id')
    amount_data = data.get('amount_data', 0)
    goal = data.get('goal').strip()
    fields = data.get('fields').strip()
    overdue_state = data.get('overdue_state', False)
    notes = data.get('notes').strip()
    test_result_selected = data.get('test_result_id', [])  # 选中的测试结果要求
    contact_id = data.get('contact_id')

    analyser = UserCredit.objects.get(id=analyser_id)
    contact = Contact.objects.get(id=contact_id)
    contact_email = contact.email
    if not contact_email:
        return JsonResponse({'msg': '选中的联系人没有email地址'})
    TestApply.objects.filter(id=test_apply_id, is_delete=False).update(analyser=analyser, amount_data=amount_data, goal=goal,
                                                      test_fields=fields, overdue_state=overdue_state,
                                                      contact=contact, progress=1, notes=notes)
    # 添加测试结果要求的manytomany关系
    test_result_list = [TestResult.objects.get(id=test_result_id) for test_result_id in test_result_selected]
    test_apply = TestApply.objects.get(id=test_apply_id, is_delete=False)
    test_apply.test_result.clear()
    test_apply.test_result.add(*test_result_list)
    # 发邮件提醒给风控经理
    try:
        email_alert([analyser.user.email], alert=1)
    except Exception as e:
        ERR_LOG.error(traceback.format_exc())
        return JsonResponse({'msg': u'向风控经理发送邮件失败:%s; 请自行通知相关风控经理处理！' % e})
    return JsonResponse({'msg': 0})


@login_required
def test_apply_view(request, testapply_id):
    try:
        test_apply = TestApply.objects.get(id=testapply_id, is_delete=False)
    except TestApply.DoesNotExist:
        raise Http404
    history_test_apply = TestApply.objects.filter(project=test_apply.project, create_time__lt=test_apply.create_time, is_delete=False)
    context = {
        'history_test_apply': history_test_apply,
        'testapply': test_apply,
        'progress_choices': TestApply.PROGRESS_CHOICES,
    }
    return render(request, 'test-apply-view.html', context)


@csrf_exempt
@login_required
def test_apply_progress_add(request, test_apply_id):
    progress = request.GET.get('progress', 1)
    description = request.GET.get('description')
    if not description:
        return JsonResponse({'msg': 'description is none'})
    try:
        test_apply = TestApply.objects.get(id=test_apply_id, is_delete=False)
    except TestApply.DoesNotExist:
        return JsonResponse({'msg': 'TestApply does not exist'})
    test_apply.progress = progress
    if int(progress) == 3:  # 测试完成
        test_apply.state = True
    test_apply.save(force_update=True)
    TestApplyProgress.objects.create(test_apply=test_apply, progress=progress, description=description,
                                     operator=request.user.first_name)
    # 如果申请被退回发邮件提醒给商务
    if int(progress) == 4:
        try:
            test_apply_refuse_email_alert([test_apply.analyser.user.email], test_apply.project.name,
                                          request.user.first_name)
        except Exception as e:
            ERR_LOG.error(traceback.format_exc())
            return JsonResponse({'msg': '向商务发送邮件提醒失败:%s' % e})
    return JsonResponse({'msg': 0})


@csrf_exempt
@login_required
def test_apply_del(request):
    try:
        test_apply_id = request.GET.get('test_apply_id')
        testap = TestApply.objects.filter(id=test_apply_id)
        for test in testap:
            test.is_delete = True
            test.save()
        testap_pro = TestApplyProgress.objects.filter(test_apply__id=test_apply_id)
        testap_pro.is_delete = True
        testap_pro.save()
    except Exception, e:
        print e
    return JsonResponse({'msg': 0})


##########################################################################
#                              交付申请
##########################################################################


@login_required
def get_project_products(request):
    project_id = request.GET.get('projectid', 0)
    try:
        project = Project.objects.get(id=project_id, is_delete=False)
    except Project.DoesNotExist as e:
        return JsonResponse({'msg': unicode(e)})
    products = project.products.exclude(name=u'营销投放').all()  # 营销投放暂不支持交付
    if not products.count():
        return JsonResponse({'msg': 'product is none!'})
    product_list = [{'name': product.name, 'id': product.id} for product in products]
    return JsonResponse({'msg': 0, 'products': product_list})


class ImpApplyListView(CommonView):
    template_name = 'imp-apply-list.html'
    allowed_role = [u'商务', u'风控经理', u'运营经理', u'交付经理', u'商务总监', u'管理层', u'交付总监']

    def get_context_data(self, **kwargs):
        context = super(ImpApplyListView, self).get_context_data(**kwargs)
        context['product_id'] = int(kwargs.get('product_id', 0))
        context['priority'] = int(kwargs.get('priority', 0))
        progress = int(kwargs.get('progress', 1))
        context['progress'] = progress
        context['page_id'] = int(self.request.GET.get('page', 1))
        context['products'] = Product.objects.all()
        context['customer_priority'] = Customer.PRIORITY_CHOICES
        context['project_name'] = ''
        imp_apply_list = ImpApply.objects.filter(is_delete=False)
        usercredit = self.request.user.usercredit
        if not usercredit.test_flag:
            imp_apply_list = imp_apply_list.exclude(applicant__test_flag=True)

        role = usercredit.role.role
        if role == u'商务':
            imp_apply_list = imp_apply_list.filter(applicant=usercredit)
        elif role == u'风控经理':
            imp_apply_list = imp_apply_list.filter(analyser=usercredit)
        elif role == u'运营经理':
            imp_apply_list = imp_apply_list.filter(operations=usercredit)
        elif role == u'交付经理':
            imp_apply_list = imp_apply_list.filter(imp_engineer=usercredit)
        elif role == u'交付总监':
            imp_apply_list = imp_apply_list.all()
        elif role == u'商务总监':
            imp_apply_list = imp_apply_list.filter(project__customer__zone=usercredit.zone)

        if context['product_id']:
            imp_apply_list = imp_apply_list.filter(product__id=context['product_id'])
        if context['priority']:
            imp_apply_list = imp_apply_list.filter(project__customer__priority=context['priority'])

        if progress == 1:
            pass
        elif progress == 2:
            imp_apply_list = imp_apply_list.filter(progress__in=[10])
        elif progress == 3:
            imp_apply_list = imp_apply_list.filter(progress=20)
        elif progress == 4:
            imp_apply_list = imp_apply_list.filter(progress=30)
        elif progress == 5:
            imp_apply_list = imp_apply_list.filter(progress=40)
        elif progress == 6:
            imp_apply_list = imp_apply_list.filter(progress__in=[45,46,47,48,49])
        elif progress == 7:
            imp_apply_list = imp_apply_list.filter(progress=50)
        elif progress == 8:
            imp_apply_list = imp_apply_list.filter(progress__in=[11, 12, 13])
        elif progress == 9:
            imp_apply_list = imp_apply_list.filter(progress__in=[44])
        
        context['imp_apply_list'] = imp_apply_list
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        imp_apply_list = context.pop('imp_apply_list')
        project_name = request.GET.get('project_name', '').strip()
        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            imp_apply_list = imp_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(imp_apply_list, context['page_id'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        imp_apply_list = context.pop('imp_apply_list')
        project_name = request.POST.get('project_name', '').strip()

        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            imp_apply_list = imp_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(imp_apply_list, context['page_id'])
        return self.render_to_response(context)


#################################
# added by 给交付总监设计的视图#
# 交付总监类视图函数开始       #
#################################
class ImpApplyDirectorListView(CommonView):
    template_name = 'imp-apply-director-list.html'
    allowed_role = [u'交付总监']

    def get_context_data(self, **kwargs):
        context = super(ImpApplyDirectorListView, self).get_context_data(**kwargs)
        context['product_id'] = int(kwargs.get('product_id', 0))
        context['priority'] = int(kwargs.get('priority', 0))
        progress = int(kwargs.get('progress', 5))
        context['progress'] = progress
        context['page_id'] = int(self.request.GET.get('page', 1))
        context['products'] = Product.objects.all()
        context['customer_priority'] = Customer.PRIORITY_CHOICES
        ##################
        #start  修改交付经理索获得的参数
        ##################
        #context['imp_engineer_list'] = UserCredit.objects.filter(role__role='交付经理')
        
        context['imp_engineer_list'] = UserCredit.objects.filter(Q(role__role='交付经理') | Q(role__role='交付总监'), test_flag = False)
        context['change_imapply_id'] = self.request.POST.get('change_imapply_id', '')
        context['change_imp_to_engineer'] = self.request.POST.get('change_imp_to_engineer', '')
        context['change_reason'] = self.request.POST.get('change_reason', '')
        ##################
        #end
        ##################
        imp_apply_list = ImpApply.objects.filter(is_delete=False)
        #context['imp_apply_list'] = imp_apply_list
        #return context
        usercredit = self.request.user.usercredit
        if not usercredit.test_flag:
            imp_apply_list = imp_apply_list.exclude(applicant__test_flag=True)
        role = usercredit.role.role
        if role == u'交付总监':
            imp_apply_list = imp_apply_list
        if context['product_id']:
            imp_apply_list = imp_apply_list.filter(product__id=context['product_id'])
        if context['priority']:
            imp_apply_list = imp_apply_list.filter(project__customer__priority=context['priority'])

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
            imp_apply_list = imp_apply_list.filter(progress__in=[45,46,47,48,49])
        elif progress == 7:
            imp_apply_list = imp_apply_list.filter(progress=50)
        elif progress == 8:
            imp_apply_list = imp_apply_list.filter(progress__in=[11, 12, 13])

        context['imp_apply_list'] = imp_apply_list
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        imp_apply_list = context.pop('imp_apply_list')
        project_name = request.GET.get('project_name', '').strip()
        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            imp_apply_list = imp_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(imp_apply_list, context['page_id'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        imp_apply_list = context.pop('imp_apply_list')
        project_name = request.POST.get('project_name', '').strip()
        if project_name:
            context['project_name'] = project_name
            context['query_param'] = query_transform(project_name=project_name)
            imp_apply_list = imp_apply_list.filter(project__name__contains=project_name)
        context['page'] = paginate(imp_apply_list, context['page_id'])
        ##################
        #start 交付总监修改交付经理code
        ##################
        try:
            imp_engineer = UserCredit.objects.filter(id = context['change_imp_to_engineer'])[0]
            impapply=ImpApply.objects.filter(id = context['change_imapply_id'],is_delete=False)[0]
            original_imp_engineer_email = impapply.imp_engineer.user.email
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
            #return JsonResponse({'msg': '向商务发送邮件提醒失败:%s' % e})

        else:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            change_log = '将项目' + impapply.project.name + ',指派给' + imp_engineer.user.first_name + ',原因是:' +context['change_reason']
            #change_log = current_time + '将项目' + '指派给' + '原因是' 
            if imp_engineer: 
                imp=ImpApply.objects.filter(id=context['change_imapply_id'],is_delete=False).update(imp_engineer = imp_engineer)
                ImpApplyProgress.objects.create(imp_apply=impapply,progress=impapply.progress,description=change_log,operator=request.user.first_name)
                send_to_impapply_email([imp_engineer.user.email],impapply.id,u"分单")
                send_to_impapply_email([original_imp_engineer_email],impapply.id,u"分单",turn_to_imp_engineer = imp_engineer.user.first_name )
              
            ##################
            #end
            ##################
        return self.render_to_response(context)
#########################
#交付总监类视图函数结束#
#########################


@login_required
def imp_modules_config(request):
    web_modules = JsonConfig.objects.filter(name='web-modules').first().value
    no_test_modules = JsonConfig.objects.filter(name='no-test').first().value
    web_modules_hnaapi = JsonConfig.objects.filter(name='web-modules-hnaapi').first().value
    return JsonResponse({'msg': 0, 'data': {'web_modules': web_modules, 'no_test': no_test_modules, 'webModules_hna_api':web_modules_hnaapi }})


class BaseImpDataParser(object):
    default_data = {}

    def __init__(self, data):
        self.date_start = data.get('imp-date-start', '')  # 建议对接开始日期
        self.target = data.get('imp-target', '0')  # 交付目的:首次对接,账号转正,套餐变更,其他
        #### add by 3.5.4
        #self.standard_fx_account = data.get('standard-fx-account', '0')  # 是否开通标准版风险罗盘账号
        ############
        self.target_note = data.get('imp-target-note', '')  # 交付目的补充说明
        self.account_type = data.get('account-type', '')  # 账号类型 '1':测试,'2':正式
        self.mode = data.getlist('imp-mode', [])  # 对接形式: Api/web
        self.multi_apply = data.get('multi-apply', '')  # 是否多次申请 '0'：否,'1':是
        self.multi_module = data.get('multi-module', '')  # 是分模块调用 '0'：否,'1':是
        self.required_key = data.get('required-key', '')  # 必填key

        self.cus_config = {
            'cus_pf': data.get('cus-pf', ''),  # 客制化评分
            'cus_data': data.get('cus-data', ''),  # 客制化数据
            'rule_blk_sheet': data.get('rule-blk-sheet', ''),  # 借款反欺诈规则-黑名单
            'rule_multi_apply': data.get('rule-multi-apply'),  # 借款反欺诈规则-多次申请
        }
        self.radar_permission = data.get('radar-permission', '')  # 雷达权限
        self.notes = data.get('notes', '')  # 备注
        self.product_id_selected = data.getlist('pgbg-m', [])  # 评估报告选择的模块
        score = data.get('score', "0")  # 评分模块选择的模块,这个是单选
        if score != "0":
            self.product_id_selected.append(score)

        self.HNApi_id_selected = data.getlist('hnapi-m', [])  # 海纳api选择的模块

        self.pgbg_product = {}
        self.HNApi_selected = {}
        # 海纳Api产品
        products = HNApiProduct.objects.filter(id__in=self.HNApi_id_selected).all()
        for p in products:
            mod = {
                'name': p.name,
                'code': p.code,
                'val': data.get('hnapi-%s-val' % p.id, 0),  # 测试总条数
                'note': data.get('hnapi-%s-note' % p.id, 0),  # 说明
            }
            self.HNApi_selected[p.id] = mod

    def construct_data(self):
        data = copy.deepcopy(self.default_data)
        for k in data.keys():
            data[k] = getattr(self, k)
            #print getattr(self, k)
        return data


class TestImpDataParser(BaseImpDataParser):
    default_data = {
        'date_start': '',
        'target': '0',
        'target_note': '',
        
        'account_type': '1',
        'mode': ['api'],
        'multi_apply': '',
        'multi_module': '',
        'required_key': 'id,cell,name,商户',
        'pgbg_product': {
            'test': {
                'api_count': 50,
                'web_count': 1000,
            },
            'product_selected': {}
        },
        'HNApi_selected': {},
        'cus_config': {
            'cus_pf': '',
            'cus_data': '',
            'rule_blk_sheet': '',
            'rule_multi_apply': '',
        },
        'radar_permission': '',
        'notes': '',
    }

    def __init__(self, data):
        super(TestImpDataParser, self).__init__(data)
        self.pgbg_product['test'] = {
            'api_count': data.get('api-count', 0),
            'web_count': data.get('web-count', 0),
        }
        # 评估报告产品
        product_selected = {}
        products = BProduct.objects.filter(id__in=self.product_id_selected).all()
        for p in products:
            mod = {
                'name': p.name,
                'code': p.code,
            }
            product_selected[p.id] = mod
        self.pgbg_product['product_selected'] = product_selected


class FormalImpDataParser(BaseImpDataParser):
    default_data = {
        'date_start': '',
        'target': '0',
        'target_note': '',
        
        'account_type': '1',
        'mode': ['api'],
        'multi_apply': '',
        'multi_module': '',
        'required_key': 'id,cell,name,商户',
        'pgbg_product': {
            'formal': {
                'free_date_start': '',  # 免费期开始日期
                'free_period': '0',  # 免费期限 0,1,2,3,4,5,6个月
                'free_limit': 0,  # 免费查询限额 xxx条
                'free_time_note': ''  # 免费期其它说明
            },
            'charge_mode': {
                'contract_start_date': '',  # 合同开始日期
                'contract_end_date': '',  # 合同截止日期
                'basic_service_charge': '',  # 基础服务费
                'mode': '',
            },
            'product_selected': {}
        },
        'HNApi_selected': {},
        'cus_config': {
            'cus_pf': '',
            'cus_data': '',
            'rule_blk_sheet': '',
            'rule_multi_apply': '',
        },
        'radar_permission': '',
        'notes': '',
        'score_price': '',
    }

    def __init__(self, data):
        super(FormalImpDataParser, self).__init__(data)
        self.score_price = data.get('score-price', '')
        self.pgbg_product['formal'] = {
            'free_date_start': data.get('free-date-start', ''),
            'free_period': data.get('free-period', ''),
            'free_limit': data.get('free-limit', 0),
            'free_time_note': data.get('free-time-note', ''),
        }
        self.pgbg_product['charge_mode'] = {
            'contract_start_date': data.get('contract-date-start', ''),
            'contract_end_date': data.get('contract-date-end', ''),
            'basic_service_charge': data.get('basic-service-charge', ''),
            'mode': '',
        }
        mode = data.get('charge-mode', ''),  # 计费模式 方案一/方案二/方案三/方案四
        mode = mode[0]
        self.pgbg_product['charge_mode'].update({'mode': mode})
        if mode == '1':
            pass
        elif mode == '2':
            hit_price = data.get('hit-price', 0)  # 每个命中客户的价格
            self.pgbg_product['charge_mode'].update({'hit_price': hit_price})
        elif mode == '3':
            fxgd_note = data.get('fxgd-note', '')  # 风险共担的模式说明
            self.pgbg_product['charge_mode'].update({'fxgd_note': fxgd_note})
        elif mode =='4':
            year_price = data.get('year-price', '') 
            month_price = data.get('month-price', '')
            self.pgbg_product['charge_mode'].update({'year_price': year_price})
            self.pgbg_product['charge_mode'].update({'month_price': month_price})

        # 评估报告产品
        product_selected = {}
        products = BProduct.objects.filter(id__in=self.product_id_selected).all()
        price_flag = mode in ['1', '3']  # 付费模式是方案二的时候,各个子模块是没有单价的
        for p in products:
            mod = {
                'name': p.name,
                'code': p.code,
            }
            if price_flag:
                # if p.type == 'score':  # 评分模块
                #     mod['price'] = self.score_price
                # else:
                mod['price'] = data.get('pgbg-%s-price' % p.id, '')
            product_selected[p.id] = mod
        self.pgbg_product['product_selected'] = product_selected


class ImpApplyAdd(CommonView):
    template_name = 'imp-apply-add.html'
    allowed_role = [u'商务']

    @staticmethod
    def init_extra_fields(mark):
        context = {
            # 风险罗盘
            'fx': TestImpDataParser.default_data,
            # 催收管理平台
            'cs': {
                'done_time': 0,           # 测试周期 0:30天; 1:60天; 2:90天; 3:180天; 4:无限制（正式账号）
                'legal_person': '',       # 企业法人
                'cszx': '',               # 测试期催收坐席
                'page_url': '',           # 公司官网
            },
        }
        return context.get(mark, {})

    def process_extra_fields(self, mark):
        post = self.request.POST
        extra_fields = dict()
        if mark == 'fx':
            account_type = post.get('account-type', '')  # 账号类型 '1':测试,'2':正式
            if account_type == '1':
                imp_data = TestImpDataParser(post)
            else:
                imp_data = FormalImpDataParser(post)

            
            extra_fields = imp_data.construct_data()
        elif mark == 'cs':
            extra_fields['done_time'] = int(post.get('done-time', 0))
            extra_fields['legal_person'] = post.get('legal-person', '')
            extra_fields['cszx'] = post.get('cszx', '')
            extra_fields['page_url'] = post.get('page_url', '')
        return extra_fields

    def get_context_data(self, **kwargs):
        self.check_role()
        context = super(ImpApplyAdd, self).get_context_data(**kwargs)
        project = Project.objects.get(id=self.args[0], is_delete=False)
        product = Product.objects.get(id=self.args[1])
        operations = UserCredit.objects.filter(role__role=u'运营经理', user__is_active=True).all()
        analysers = UserCredit.objects.filter(role__role=u'风控经理', user__is_active=True).all()
        deliverys = UserCredit.objects.filter(role__role=u'交付经理', user__is_active=True).all()
        if not self.request.user.usercredit.test_flag:
            operations = operations.exclude(test_flag=True)
            analysers = analysers.exclude(test_flag=True)
        history_imp_apply = ImpApply.objects.filter(project=project, is_delete=False).order_by('-create_time')
        context.update({
            'project': project,
            'product': product,
            'analysers': analysers,
            'operations': operations,
            'deliverys': deliverys,
            'contacts': project.contacts.all(),
            'history_imp_apply': history_imp_apply,
            'data_modules': BProduct.get_data_dict(),
            'hnapi_modules': HNApiProduct.objects.all(),
        })
        context.update(self.init_extra_fields(context['product'].mark))

        if history_imp_apply:
            imp_apply = history_imp_apply[0]
            context.update({
            'imp_apply': imp_apply,
            'project': imp_apply.project,
            'product': imp_apply.product,
            'analyser_selected': imp_apply.analyser,
            'operations_selected': imp_apply.operations,
            'deliverys_selected': imp_apply.imp_engineer,
            'contact_selected': imp_apply.contact,
            })
            extra_fields = imp_apply.extra_fields
            extra_fields['HNApi_selected'] = {int(k): v for k, v in extra_fields['HNApi_selected'].items()}
            pgbg_product = extra_fields['pgbg_product']
            pgbg_product['product_selected'] = {int(k): v for k, v in pgbg_product['product_selected'].items()}
            context.update(imp_apply.extra_fields)
            context['multi_apply'] = ''
            context['multi_module'] = ''
        else:
            context['multi_apply'] = ''
            context['multi_module'] = ''
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.check_role()
            apiFileUpload_dz = request.POST.get('apiFileUpload_dz', '')
            apiFileUpload_specialList = request.POST.get('apiFileUpload_specialList' ,'')
            print apiFileUpload_dz,apiFileUpload_specialList
            context = self.get_context_data(**kwargs)
            action = request.POST.get('action', '')  # 提交/保存
            progress = 30 if action == 'submit' else 10
            images = request.FILES.get('email-pic')
            analyser_id = request.POST.get('analyser', 0)
            contact_id = request.POST.get('contact', 0)
            operations_id = request.POST.get('operations', 0)
            deliverys_id = request.POST.get('deliverys', 0)
            analyser = UserCredit.objects.filter(id=analyser_id).first()
            context['analyser_selected'] = analyser
            operations = UserCredit.objects.filter(id=operations_id).first()
            deliverys = UserCredit.objects.filter(id=deliverys_id).first()
            context['operations_selected'] = operations
            contact = Contact.objects.filter(id=contact_id).first()
            context['contact_selected'] = contact
            extra_fields = self.process_extra_fields(context['product'].mark)
            extra_fields['apiFileUpload_specialList'] = apiFileUpload_specialList
            extra_fields['apiFileUpload_dz'] = apiFileUpload_dz
            #extra_fields["standard_fx_account"] = request.POST.get('standard-fx-account', '') 
            if progress == 30:
                try:
                    latest_imp_apply = ImpApply.objects.filter(project__customer=context['project'].customer, state=True, is_delete=False)\
                        .latest('modify_time')
                    extra_fields['apicode'] = latest_imp_apply.extra_fields.get('apicode', '')
                except Exception, e:
                    extra_fields['apicode'] = ""
            imp = ImpApply.objects.create(applicant=request.user.usercredit, analyser=analyser, operations=operations,
                                    imp_engineer=deliverys, project=context['project'], product=context['product'],
                                    extra_fields=extra_fields, contact=contact, pic=images, progress=progress)
            if progress == 30:
                try:
                    #email_alert([analyser.user.email], alert=2)  # 邮件提醒风控经理审核
                    send_to_impapply_email([analyser.user.email,operations.user.email],imp.id ,email_type = u"交付申请")
                except Exception:
                    ERR_LOG.error(traceback.format_exc())
                    messages.info(request, u'系统向风控经理发送邮件失败, 请另行通知风控经理审核申请')
        except Exception, e:
            print 22222,traceback.format_exc()

        return redirect(reverse('imp-apply-list', kwargs={'progress': 1, 'priority': 0, 'product_id': 0}))


class ImpApplyEdit(CommonView):
    template_name = 'imp-apply-edit.html'
    allowed_role = [u'商务']

    def get_context_data(self, **kwargs):
        context = super(ImpApplyEdit, self).get_context_data(**kwargs)
        imp_apply = ImpApply.objects.get(id=self.args[0], is_delete=False)
        analysers = UserCredit.objects.filter(role__role=u'风控经理', user__is_active=True).all()
        operations = UserCredit.objects.filter(role__role=u'运营经理', user__is_active=True).all()
        deliverys = UserCredit.objects.filter(role__role=u'交付经理', user__is_active=True).all()
        if not self.request.user.usercredit.test_flag:
            analysers = analysers.exclude(test_flag=True)
            operations = operations.exclude(test_flag=True)
            deliverys = deliverys.exclude(test_flag=True)
        context.update({
            'imp_apply': imp_apply,
            'project': imp_apply.project,
            'product': imp_apply.product,
            'analysers': analysers,
            'analyser_selected': imp_apply.analyser,
            'operations': operations,
            'deliverys': deliverys,
            'operations_selected': imp_apply.operations,
            'deliverys_selected': imp_apply.imp_engineer,
            'contacts': imp_apply.project.contacts.all(),
            'contact_selected': imp_apply.contact,
            'data_modules': BProduct.get_data_dict(),
            'hnapi_modules': HNApiProduct.objects.all(),
        })
        # HNApi_selected和product_selected字典中的的key本来是id（数字）,但转换成json再转回来之后就变成字符串类型了
        # 下面是把字符串再转回数字,方便在模板中用in判断
        extra_fields = imp_apply.extra_fields
        extra_fields['HNApi_selected'] = {int(k): v for k, v in extra_fields['HNApi_selected'].items()}
        pgbg_product = extra_fields['pgbg_product']
        pgbg_product['product_selected'] = {int(k): v for k, v in pgbg_product['product_selected'].items()}
        context.update(imp_apply.extra_fields)
        return context

    def process_extra_fields(self, mark):
        post = self.request.POST
        extra_fields = dict()
        if mark == 'fx':
            account_type = post.get('account-type', '')  # 账号类型 '1':测试,'2':正式
            if account_type == '1':
                imp_data = TestImpDataParser(post)
            else:
                imp_data = FormalImpDataParser(post)
            extra_fields = imp_data.construct_data()
        elif mark == 'cs':
            extra_fields['done_time'] = int(post.get('done-time', 0))
            extra_fields['legal_person'] = post.get('legal-person', '')
            extra_fields['cszx'] = post.get('cszx', '')
            extra_fields['page_url'] = post.get('page_url', '')
        return extra_fields

    def post(self, request, *args, **kwargs):
        self.check_role()
        imp_apply = ImpApply.objects.get(id=args[0], is_delete=False)
        action = request.POST.get('action', '')  # 提交/保存
        progress = 30 if action == 'submit' else 10
        images = request.FILES.get('email-pic')
        analyser_id = request.POST.get('analyser', 0)
        contact_id = request.POST.get('contact', 0)
        operations_id = request.POST.get('operations', 0)
        deliverys_id = request.POST.get('deliverys', 0)
        analyser = UserCredit.objects.filter(id=analyser_id).first()
        operations = UserCredit.objects.filter(id=operations_id).first()
        deliverys = UserCredit.objects.filter(id=deliverys_id).first()
        contact = Contact.objects.filter(id=contact_id).first()
        extra_fields = self.process_extra_fields(imp_apply.product.mark)
        imp_apply.imp_engineer = deliverys
        imp_apply.analyser = analyser
        imp_apply.contact = contact
        imp_apply.operations = operations
        imp_apply.progress = progress
        if images:
            imp_apply.pic = images
        if progress == 30:
            try:
                latest_imp_apply = ImpApply.objects.filter(project__customer=imp_apply.project.customer, state=True, is_delete=False).latest('modify_time')
                extra_fields['apicode'] = latest_imp_apply.extra_fields.get('apicode', '')
            except Exception, e:
                extra_fields['apicode'] = ""
        imp_apply.extra_fields = extra_fields
        imp_apply.save()
        if progress == 30:
            im = ImpApplyProgress.objects.create(imp_apply=imp_apply, progress=20, description="申请",
                                            operator=request.user.first_name)
            try:
                #email_alert([analyser.user.email], alert=2)  # 邮件提醒风控经理审核
                send_to_impapply_email([analyser.user.email,operations.user.email],imp_apply.id,email_type = u"交付申请")
            except Exception as e:
                ERR_LOG.error(traceback.format_exc())
                messages.info(request, u'系统向风控经理发送邮件失败, 请自行通知风控经理审核申请.'+unicode(e))
        return redirect(reverse('imp-apply-list', kwargs={'progress': 1, 'priority': 0, 'product_id': 0}))




@login_required
def imp_apply_view(request, imp_apply_id):
    deliver_status = request.GET.get("deliver_status",0)
    deliver_description = request.GET.get("description",0)
    imp_apply = get_object_or_404(ImpApply, id=imp_apply_id)
    context = {}
    ##################
    #start 更新状态 和添加描述code
    ##################
    if imp_apply :
        if deliver_status != 0 and deliver_description:
            deliver_status=int(deliver_status)
            all_status_in_impapply=dict(ImpApply.PROGRESS_CHOICES)
            change_log = '将项目' + imp_apply.project.name + ',状态修改为:' + all_status_in_impapply[deliver_status] + ',描述是:' + deliver_description
            #current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            ImpApply.objects.filter(id = imp_apply_id ,is_delete=False).update(progress = deliver_status)
            ImpApplyProgress.objects.create(imp_apply = imp_apply,progress = deliver_status,description = change_log,operator = request.user.first_name)
            #context['complete_modified_singal'] = "complete_modified_singal"
            imp_apply = get_object_or_404(ImpApply, id=imp_apply_id)
        elif deliver_status == 0 and deliver_description !=0 :
            change_log = '将项目' + imp_apply.project.name + '添加新的消息为:' + deliver_description
            ImpApplyProgress.objects.create(imp_apply = imp_apply,progress = imp_apply.progress,description = change_log,operator = request.user.first_name)
            imp_apply = get_object_or_404(ImpApply, id=imp_apply_id)
    ##################
    #end
    ##################
    history_imp_apply = ImpApply.objects.filter(project=imp_apply.project, create_time__lt=imp_apply.create_time, is_delete=False)
    context = {
        'imp_apply': imp_apply,
        'history_imp_apply': history_imp_apply,
        
    }
    return render(request, 'imp-apply-view.html', context)



@login_required
def imp_apply_free_date_start_edit(request, imp_apply_id):
    free_date_start = request.GET.get('date', '')
    if not free_date_start:
        return JsonResponse({'msg': u'参数错误'})
    imp_apply = get_object_or_404(ImpApply, id=imp_apply_id)
    extra_fields = imp_apply.extra_fields
    extra_fields['pgbg_product']['formal'].update({'free_date_start': free_date_start})
    imp_apply.extra_fields = extra_fields
    imp_apply.save(force_update=True)
    return JsonResponse({'msg': 0})


@login_required
def imp_apply_del(request):
    imp_apply_id = request.GET.get('imp_apply_id', 0)
    imp = ImpApply.objects.get(id=imp_apply_id)
    imp.is_delete = True
    imp.save()
    try:
        imp_pro = ImpApplyProgress.objects.get(imp_apply__id=imp_apply_id)
        imp_pro.delete = True
        imp_pro.save()
    except Exception, e:
        print e
    return JsonResponse({'msg': 0})


@login_required
def imp_apply_progress_add(request, imp_apply_id):
    user_name = request.user.first_name
    try:
        progress = int(request.GET.get('progress', 1))
    except ValueError as e:
        return JsonResponse({'msg': unicode(e)})
    description = request.GET.get('description', u'"无"')
    try:
        imp_apply = ImpApply.objects.get(id=imp_apply_id, is_delete=False)
        imp_apply.progress = progress
        
    except ImpApply.DoesNotExist:
        return JsonResponse({'msg': 'ImpApply does not exist'})
    
	
    print progress,imp_apply.progress
    try:
        if progress == 11:
            #imp_apply_refuse_email_alert([imp_apply.applicant.user.email], imp_apply.project.name,
            #                             imp_apply.product.name, request.user.first_name)
            return_to_applicant_email([imp_apply.applicant.user.email],imp_apply.id ,email_type = u"退回邮件" ,returned_person = user_name ,turn_reason = description)
        elif progress == 12:
            # imp_apply_refuse_email_alert([imp_apply.applicant.user.email, imp_apply.analyser.user.email],
            #                              imp_apply.project.name, imp_apply.product.name, request.user.first_name)
            return_to_applicant_email([imp_apply.applicant.user.email, ],imp_apply.id ,email_type = u"退回邮件", returned_person = user_name ,turn_reason = description)
            
        elif progress == 13:
            emails = [imp_apply.applicant.user.email,]
            #imp_apply_refuse_email_alert(emails, imp_apply.project.name, imp_apply.product.name,
                                         #request.user.first_name)
            return_to_applicant_email(emails,imp_apply.id ,email_type = u"退回邮件" ,returned_person = user_name ,turn_reason = description)
        elif progress == 30:
            #email_alert([imp_apply.operations.user.email], alert=2)
            send_to_impapply_email([imp_apply.operations.user.email],imp_apply.id,email_type = u"交付申请")
        elif progress == 40:
            #email_alert([imp_apply.imp_engineer.user.email], alert=3)
            send_to_impapply_email([imp_apply.imp_engineer.user.email],imp_apply.id,email_type = u"交付申请")
        ########
        # added by guo 
        #########
        elif progress == 44:
            turn_to_applicant_email([imp_apply.applicant.user.email],imp_apply.id ,email_type = u'指回',returned_person = user_name)
        
        elif progress == 50:
            #imp_apply_done_email_alert([imp_apply.applicant.user.email], imp_apply.project.name, imp_apply.product.name)
            send_to_impapply_email([imp_apply.applicant.user.email],imp_apply.id,email_type = "交付完成")
            imp_apply.state = True  # 交付完成
    except Exception as e:
        ERR_LOG.error(traceback.format_exc())
        messages.info(request, u'系统邮件提醒发送失败'+unicode(e))
    imp_apply.save()
    ImpApplyProgress.objects.create(imp_apply=imp_apply, progress=progress, description=description,
                                    operator=request.user.first_name)

    return JsonResponse({'msg': 0})


@require_POST
@csrf_exempt
def imp_apply_done(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'msg': 'DataError'})
    try:
        imp_apply_id = data['id']
        api_code = data['apicode']
    except KeyError:
        return JsonResponse({'msg': 'KeyError'})
    if not api_code:
        return JsonResponse({'msg': 'ApiCodeError'})
    try:
        imp_apply = ImpApply.objects.get(id=imp_apply_id, is_delete=False)
    except ImpApply.DoesNotExist:
        return JsonResponse({'msg': 'IdError'})
    imp_apply.progress = 46
    #imp_apply.state = True
    extra_fields = imp_apply.extra_fields
    extra_fields['apicode'] = api_code
    imp_apply.extra_fields = extra_fields
    imp_apply.save()
    try:
        pass
        #imp_apply_done_email_alert([imp_apply.applicant.user.email], imp_apply.project.name, imp_apply.product.name)
    except Exception:
        ERR_LOG.error(traceback.format_exc())
    ImpApplyProgress.objects.create(imp_apply=imp_apply, progress=46, description=u'开通账号', operator=u'API后台')
    return JsonResponse({'msg': 'done'})


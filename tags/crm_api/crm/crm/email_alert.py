# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback
import  logging
from django.core.mail import EmailMessage
from django.conf import settings
from .models import ImpApply,TestApply
ERR_LOG = logging.getLogger('crm_error')

SUBJECT_T = u"【CRM系统邮件】"

CONTENT_T_1 = "<h4>--------测试申请---------</h4><br>" \
              """<p>您有一个测试申请需要处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""

CONTENT_T_2 = "<h4>--------交付申请【审核】---------</h4><br>" \
              """<p>您有一个交付申请待审核, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""

CONTENT_T_3 = "<h4>--------交付申请---------</h4><br>" \
              """<p>您有一个交付申请需要处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""

CONTENT_T_4 = "<h4>项目：{0}的测试申请被【{1}】退回了</h4><br>" \
              """<p><a href="http://crm.100credit.cn">CRM系统</a></p>"""

CONTENT_T_5 = "<h4>您的项目：{0} -- 产品：{1}交付申请被【{2}】退回了</h4><br>" \
              """<p><a href="http://crm.100credit.cn">CRM系统</a></p>"""

CONTENT_T_6 = "<h4>您的项目：{0} -- 产品：{1}交付申请已经交付完成</h4><br>" \
              """<p>如果不是您本人操作请登录 <a href="http://crm.100credit.cn">CRM系统</a>查看</p>"""

CONTENT = {
    1: CONTENT_T_1,
    2: CONTENT_T_2,
    3: CONTENT_T_3,
}


def _send_html_mail(subject, html_content, recipient_list):
    """ 发送html内容的邮件 """
    msg = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html"  # main content is now text/html
    msg.send(fail_silently=True)


def email_alert(recipient_list, alert=1):
    _send_html_mail(SUBJECT_T, CONTENT[alert], recipient_list)


def imp_apply_done_email_alert(recipient_list, project, product):
    _send_html_mail(SUBJECT_T, CONTENT_T_6.format(project, product), recipient_list)


def test_apply_refuse_email_alert(recipient_list, project_name, operator):
    _send_html_mail(SUBJECT_T, CONTENT_T_4.format(project_name, operator), recipient_list)


def imp_apply_refuse_email_alert(recipient_list, project, product, operator):
    _send_html_mail(SUBJECT_T, CONTENT_T_5.format(project, product, operator), recipient_list)



def send_to_impapply_email(recipient_list,imp_id,email_type = "通知",turn_to_imp_engineer = ''):
    im = ImpApply.objects.filter(id = int(imp_id))[0]
    if im :
        title = "%s # %s 【 %s】  【 %s】  %s  %s-%s-%s-%s "%( email_type,
                                                            im.id , 
                                                            im.project.customer.name ,
                                                            im.project.name,
                                                            im.project.customer.zone.name, 
                                                            im.applicant.user.first_name ,
                                                            im.analyser.user.first_name,
                                                            im.operations.user.first_name,
                                                            im.imp_engineer.user.first_name,
                                                                            )
     
             
        content = title + """ \n  <h5>您有一个工单需要处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</h5>""" 
        if turn_to_imp_engineer :
            content = title + """ \n  <h5>您有一个工单被交付总监指给了交付经理 %s</h5>"""%turn_to_imp_engineer
            content = content + """ \n  <h5>如需查看, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</h5>""" 
        if email_type == '交付完成':
            content = ''
            content = title + "\n" + CONTENT_T_6.format(im.project.name, im.product.name)
        imp_product_and_hnapi_info = get_imp_product_and_hnapi_info(im)
        content = content + imp_product_and_hnapi_info[0] +  "\n" + imp_product_and_hnapi_info[1]
        _send_html_mail(title, content, recipient_list)

def return_to_applicant_email(recipient_list,imp_id ,email_type = u"退回",returned_person = '',turn_reason = u'无'):
    ######################
    # 退回的邮件
    ######################
    im = ImpApply.objects.filter(id = int(imp_id))[0]
    if im :
        progress = dict(ImpApply.PROGRESS_CHOICES)
        account_type = '正式' if im.extra_fields.get('account_type')=='2' else '测试'
        title = " %s# %s 【 %s】 【 %s】  %s  %s %s-%s-%s-%s "%(email_type ,im.id , 
                                            im.project.customer.name ,
					                        im.project,
                                            im.project.customer.zone.name, 
                                            account_type,
                                            im.applicant.user.first_name ,
                                            im.analyser.user.first_name,
                                            im.operations.user.first_name,
                                            im.imp_engineer.user.first_name,
                                                            )
        # try:
        #     turn_reason = im.get_latest_progress().description
        # except Exception, e:
        #     ERR_LOG.error(traceback.format_exc())
        #     turn_reason = ''
        content = title +  """\n <p>您有一个crm工单被 %s 退回了,原因是 %s  请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""%(returned_person,turn_reason)
        imp_product_and_hnapi_info = get_imp_product_and_hnapi_info(im)
        content = content + imp_product_and_hnapi_info[0] +  "\n" + imp_product_and_hnapi_info[1]   
        _send_html_mail(title, content, recipient_list)

def send_to_test_email(recipient_list,test_id ,email_type = u'测试'):
    test_ob = TestApply.objects.filter(id = int(test_id))[0]
    print test_ob
    if test_ob:
        title = "%s#%s %s [%s] %s %s"%(email_type,test_ob.id , 
                              test_ob.dts_account,
                              test_ob.project.customer.name ,
                              test_ob.applyman.user.first_name ,
                              test_ob.analyser.user.first_name,
                              )
        content = title + """ \n <p>你有一个crm测试工单，请及时处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""
        #imp_product_and_hnapi_info = get_imp_product_and_hnapi_info(test_ob)
        #content = content  +  "\n" + imp_product_and_hnapi_info[1] 
        _send_html_mail(title, content , recipient_list)


def turn_to_applicant_email(recipient_list,imp_id ,email_type = u'指回',returned_person = ''):
    #############################
    #交付指回crm工单发的邮件内容
    #############################
    im = ImpApply.objects.filter(id = int(imp_id))[0]
    if im :
        progress = dict(ImpApply.PROGRESS_CHOICES)
        account_type = '正式' if im.extra_fields.get('account_type')=='2' else '测试'
        title = "%s# %s 【 %s】  【 %s】  %s %s %s-%s"%( email_type, im.id ,
                                    im.project.name, 
                                    im.project.customer.name ,
                                    im.project.customer.zone.name, 
                                    account_type,
                                    im.applicant.user.first_name ,
                                    im.imp_engineer.user.first_name,
                                                    )
        content = title  +  """ \n <p>您有个crm工单被%s  指回来了，若需要对工单更新，请及时处理  请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""%returned_person
        imp_product_and_hnapi_info = get_imp_product_and_hnapi_info(im)
        content = content + imp_product_and_hnapi_info[0] +  "\n" + imp_product_and_hnapi_info[1]
        _send_html_mail(title, content, recipient_list)


def get_imp_product_and_hnapi_info(impapply):
    extra_fields = impapply.extra_fields
    report_string = '<dl><dt><h5>交付的评估报告系列产品</h5></dt>'
    if extra_fields.get("pgbg_product") and extra_fields.get("pgbg_product").get("product_selected").values():
        for p in extra_fields.get("pgbg_product").get("product_selected").values():
             report_string = report_string + "<dd>" + p.get("name") + '（'+ p.get("code") +'）' +'</dd>' 
             if p.get("price"):
                report_string = report_string[:-5]
                report_string = report_string +'单价（元）'+'：'+ p.get("price") +'</dd>' 
    report_string = report_string + '</dl>'
    imp_HNApi = '<dl><dt><h5>交付的海纳api产品</h5></dt>'
    if extra_fields.get("HNApi_selected") and extra_fields.get("HNApi_selected").values():
        for p in extra_fields.get("HNApi_selected").values():
            if extra_fields.get("account_type") == "1":
                imp_HNApi = imp_HNApi + '<dd>' + p.get("name") +  '；' + '测试条数：' + p.get("val") + '说明：' +  p.get("note") +"</dd>"
            else:
                imp_HNApi = imp_HNApi + '<dd>' + p.get("name") +  '；' + '单价（元）：' + p.get("val") + '说明：' +  p.get("note") + "</dd>"
    imp_HNApi = imp_HNApi + '</dl>'
    return report_string,imp_HNApi

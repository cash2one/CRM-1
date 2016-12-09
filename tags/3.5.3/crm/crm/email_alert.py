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

CONTENT_T_5 = "<h4>项目：{0} -- 产品：{1}交付申请被【{2}】退回了</h4><br>" \
              """<p><a href="http://crm.100credit.cn">CRM系统</a></p>"""

CONTENT_T_6 = "<h4>项目：{0} -- 产品：{1}交付申请已经交付完成</h4><br>" \
              """<p><a href="http://crm.100credit.cn">CRM系统</a></p>"""

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



def send_to_impapply_email(recipient_list,imp_id,email_type = u"通知",turn_to_imp_engineer = ''):
    im = ImpApply.objects.filter(id = int(imp_id))[0]
    if im :
        title = "%s # %s 【 %s】  【 %s】  %s  %s-%s-%s-%s "%( email_type,im.id , 
                                                            im.project.customer.name ,
                                                            im.project.name,
                                                            im.project.customer.zone.name, 
                                                            im.applicant ,
                                                            im.analyser,
                                                            im.operations,
                                                            im.imp_engineer,
                                                                            )
     
             
        content = title + """ \n  <h5>您有一个工单需要处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</h5>""" 
        if turn_to_imp_engineer :
            content = title + """ \n  <h5>您有一个工单被交付总监指给了交付经理 %s</h5>"""%turn_to_imp_engineer
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
                                            im.applicant ,
                                            im.analyser,
                                            im.operations,
                                            im.imp_engineer,
                                                            )
        # try:
        #     turn_reason = im.get_latest_progress().description
        # except Exception, e:
        #     ERR_LOG.error(traceback.format_exc())
        #     turn_reason = ''
        content = title +  """\n <p>您有一个crm工单被 %s 退回了,原因是 %s  请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""%(returned_person,turn_reason)
      
        _send_html_mail(title, content, recipient_list)

def send_to_test_email(recipient_list,test_id ,email_type = u'测试'):
    test_ob = TestApply.objects.filter(id = int(test_id))[0]
    print test_ob
    if test_ob:
        title = "%s#%s %s [%s] %s %s"%(email_type,test_ob.id , 
                              test_ob.dts_account,
                              test_ob.project.customer.name ,
                              test_ob.applyman ,
                              test_ob.analyser,
                              )
        content = title + """ \n <p>你有一个crm测试工单，请及时处理, 请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""
     
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
                                    im.applicant ,
                                    im.imp_engineer,
                                                    )
        content = title  +  """ \n <p>您有个crm工单被%s  指回来了，若需要对工单更新，请及时处理  请登录<a href="http://crm.100credit.cn">CRM系统</a>确认并处理.</p>"""%returned_person
        _send_html_mail(title, content, recipient_list)

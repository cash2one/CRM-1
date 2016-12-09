# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.conf import settings


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

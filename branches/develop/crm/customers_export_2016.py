# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import  codecs
import csv,os 
import django
from crm.models import ImpApply
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")
##########################################################
# 2016.10.17 叶美女提出运营需要导出交付申请的联系人的信息#
# 导出会在windows  乱码 可以用txt 打开 另存为 格式为ansi 再用
#  office 打开即可
##########################################################
# Django 版本>=1.7时,需要加下面两句,否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
if django.VERSION >= (1, 7):
    django.setup()


def export_customers_data():
    impapply_list = ImpApply.objects.filter(is_delete=False)
    customers_data = open("customers_data.csv", 'wb')
    customers_data.write(codecs.BOM_UTF8)
    writer = csv.writer(customers_data)
    header = [
        '交付单号','客户名称','项目名称', 
        '联系人姓名','联系人电话',
        '联系人邮箱', 
        '商务名',
        '商务所在区域', 'apicode' ,

    ]


    writer.writerow(header)
    #csvfile.write_row(header)
    for imp_apply in impapply_list:
        mobile = ''
        email = ''
        contact_name = ''
        apicode = str(imp_apply.extra_fields.get('apicode',''))
        if imp_apply.contact:
            mobile = imp_apply.contact.mobile
            email = imp_apply.contact.email
            contact_name = imp_apply.contact.name

        row = [str(imp_apply.id) ,imp_apply.project.customer.name,imp_apply.project.name,
              contact_name, mobile, 
              email, 
              imp_apply.applicant.user.first_name,
              imp_apply.applicant.zone.name ,apicode]
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            writer.writerow([imp_apply.encode('utf-8') for imp_apply in row])
    customers_data.close()




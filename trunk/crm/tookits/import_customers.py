# -*- coding: utf-8 -*-

import os
import csv
import codecs
import traceback
import xlrd
from readxls import read_xls

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")

# Django 版本>=1.7时，需要加下面两句,否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
import django
if django.VERSION >= (1, 7):
    django.setup()

from django.contrib.auth.models import User
from crm.models import (Customer, CustomerCategory1, CustomerCategory2, CustomerCategory3, CustomerType,
                        ImpApply, Project, Product)
from accounts.models import UserCredit


book = xlrd.open_workbook('/home/baixue/100credit/CRMData/customers.xls')


# print '----------------------------------------------'
# print u'更新客户简称，三级类目'
# print '----------------------------------------------'
#
# data = read_xls(book, u'根据客户全称更新客户简称，三级类目')

# no_customer = open('no_customers.csv', 'wb')
# no_customer.write(codecs.BOM_UTF8)
# writer = csv.writer(no_customer)
#
# for d in data:
#     customer = Customer.objects.filter(name=d[0]).first()
#     if customer:
#         customer.short_name = d[3]
#         if d[4]:
#             customer.category1 = CustomerCategory1.objects.filter(name=d[4]).first()
#             if d[5]:
#                 customer.category2 = CustomerCategory2.objects.filter(name=d[5]).first()
#                 if d[6]:
#                     customer.category3 = CustomerCategory3.objects.filter(name=d[6]).first()
#         customer.save()
#     else:
#         print d[0]
#         writer.writerow(d)
#
# no_customer.close()
# print '----------------------------------------------'
# print u'DONE'
# print '----------------------------------------------'


# print '----------------------------------------------'
# print u'根据客户id更新客户全称'
# print '----------------------------------------------'
#
# data = read_xls(book, u'根据客户id更新客户全称')
#
# for d in data:
#     customer = Customer.objects.filter(id=d[1]).first()
#     if customer:
#         customer.name = d[0]
#         customer.save()
#     else:
#         print d[0]
# print '----------------------------------------------'
# print u'DONE'
# print '----------------------------------------------'


# print '----------------------------------------------'
# print u'根据客户ID更新客户级别'
# print '----------------------------------------------'
#
# data = read_xls(book, u'根据客户ID更新客户级别')
#
# for d in data:
#     customer = Customer.objects.filter(id=d[1]).first()
#     if customer:
#         if d[0] == u'公司级重点客户':
#             customer.priority = 1
#         elif d[0] == u'区域级重点客户':
#             customer.priority = 2
#         else:
#             print 'error'
#         customer.save()
#     else:
#         print d[0]
# print '----------------------------------------------'
# print u'DONE'
# print '----------------------------------------------'


# print '----------------------------------------------'
# print u'导入新客户1'
# print '----------------------------------------------'
#
# book1 = xlrd.open_workbook('/home/baixue/100credit/CRMData/customers1.xls')
# data = read_xls(book1, u'签合同但crm没有的客户')
# PRIORITY_MAP = {u'公司级重点客户': 1, u'区域级重点客户': 2, u'非重点客户': 3}
#
# for d in data:
#     customer_type = CustomerType.objects.filter(name=d[1]).first()
#     user = User.objects.filter(first_name=d[7]).first()
#     category1 = CustomerCategory1.objects.filter(name=d[5]).first()
#     category2 = CustomerCategory2.objects.filter(name=d[6]).first()
#     category3 = CustomerCategory3.objects.filter(name=d[7]).first()
#     priority = PRIORITY_MAP.get(d[3], 3)
#     province = d[4]
#     city = d[5] or 'null'
#     address = d[6] or ''
#     try:
#         if Customer.objects.filter(name=d[2]).exists():
#             print d[2], 'exists'
#             continue
#         customer = Customer.objects.create(name=d[2], short_name=d[4], type=customer_type,
#                                            priority=priority, zone=user.usercredit.zone,
#                                            registered_capital=0, shareholder='null', product_desc='null',
#                                            province=province, city=city, address=address,
#                                            category1=category1, category2=category2, category3=category3)
#         customer.businessman.add(user.usercredit)
#     except Exception:
#         print 'error', d[2]
#         traceback.print_exc()
#         continue
#
# print '----------------------------------------------'
# print u'DONE'
# print '----------------------------------------------'


# print '----------------------------------------------'
# print u'导入新客户2'
# print '----------------------------------------------'
#
# book1 = xlrd.open_workbook('/home/baixue/100credit/CRMData/customers1.xls')
# data = read_xls(book1, u'交付系统有的客户但crm系统没有客户')
#
# for d in data:
#     customer_type = CustomerType.objects.filter(name=d[0]).first()
#     user = User.objects.filter(first_name=d[3]).first()
#     category1 = CustomerCategory1.objects.filter(name=d[9]).first()
#     category2 = CustomerCategory2.objects.filter(name=d[10]).first()
#     category3 = CustomerCategory3.objects.filter(name=d[11]).first()
#     province = d[6]
#     city = d[7] or 'null'
#     address = d[8] or ''
#     try:
#         if Customer.objects.filter(name=d[1]).exists():
#             print d[1], 'exists'
#             continue
#         customer = Customer.objects.create(name=d[1], short_name=d[2], type=customer_type,
#                                            priority=3, zone=user.usercredit.zone,
#                                            registered_capital=0, shareholder='null', product_desc='null',
#                                            province=province, city=city, address=address,
#                                            category1=category1, category2=category2, category3=category3)
#         customer.businessman.add(user.usercredit)
#     except Exception:
#         print 'error', d[1]
#         traceback.print_exc()
#         continue
#
# print '----------------------------------------------'
# print u'DONE'
# print '----------------------------------------------'


print '----------------------------------------------'
print u'所有用户评估报告的项目迁移到风险罗盘'
print '----------------------------------------------'

product_pgbg = Product.objects.filter(name=u'用户评估报告').first()
product_fx = Product.objects.filter(name=u'风险罗盘').first()
projects = Project.objects.filter(products=product_pgbg).all()
for p in projects:
    p.products.remove(product_pgbg)
    p.products.add(product_fx)

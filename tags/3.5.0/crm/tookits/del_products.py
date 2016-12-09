# -*- coding: utf-8 -*-

""" 修改反欺诈产品相关的项目和交付申请 """

import os
import csv
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")

# Django 版本>=1.7时,需要加下面两句,否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
if django.VERSION >= (1, 7):
    django.setup()

from crm.models import Project, Product, ImpApply, TestApply

# {
#   "num_day": 500,
#   "account": "58tongcheng"
# }
#
# {
#   "done_time": 4,
#   "num_day": 999999,
#   "free_day": 0,
#   "data_modules": [],
#   "module_price_desc": ""
# }


# csv.reader
csvfile = file('impapply.csv', 'rb')
reader = csv.reader(csvfile)

for line in reader:
    impapply_id = line[0]
    dm_id = line[1:]
    if dm_id:
        imp = ImpApply.objects.get(id=impapply_id)
        imp.set_extra_field('data_modules', dm_id)
        imp.save()

csvfile.close()

# product_src = Product.objects.get(name=u'反欺诈产品')
# product_rel = Product.objects.get(name=u'用户评估报告')
#
# projects = Project.objects.filter(products__name=u'反欺诈产品').all()
#
# for project in projects:
#     print project.name
#     project.products.add(product_rel)
#     project.products.remove(product_src)
#
#
# # 将交付申请的反欺诈产品也改成用户评估报告
# imps = ImpApply.objects.filter(product=product_src)
#
# for imp in imps:
#     imp.product = product_rel
#     imp.save()

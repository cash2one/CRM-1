# -*- coding: utf-8 -*-

"""导出数据"""

import os
import csv
import codecs
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")

# Django 版本>=1.7时,需要加下面两句,否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
if django.VERSION >= (1, 7):
    django.setup()

from crm.models import Customer


customers = Customer.objects.all(is_delete=False)


fobj = open("customers.csv", 'wb')
fobj.write(codecs.BOM_UTF8)
writer = csv.writer(fobj)
writer.writerow(['id', '客户名称', '客户简称', '区域', '商务'])
for c in customers:
    row = [str(c.id), c.name, c.short_name, c.zone.name, c.get_businessmans_name()]
    try:
        writer.writerow(row)
    except UnicodeEncodeError:
        writer.writerow([c.encode('utf-8') for c in row])


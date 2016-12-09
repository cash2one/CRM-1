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

from crm.models import Customer, ImpApply, Project




fobj = open("customers.csv", 'wb')
fobj.write(codecs.BOM_UTF8)
writer = csv.writer(fobj)
writer.writerow([
    'apicode', 'id', '客户名称', '客户简称', '类型', '一级类目', '二级类目', '三级类目', '客户级别', '区域', '省份', '城市', '详细地址',
    '跟进商务', '注册资本', '股东', '产品描述', '备注', '创建时间'
])

for c in ImpApply.objects.all():
    extra_fields = c.extra_fields
    if 'apicode' in extra_fields:
        if extra_fields['apicode']:
            c1 = c.project.customer.category1.name if c.project.customer.category1 else ''
            c2 = c.project.customer.category2.name if c.project.customer.category2 else ''
            c3 = c.project.customer.category3.name if c.project.customer.category3 else ''
            row = [
                extra_fields['apicode'],
                str(c.project.customer.id), c.project.customer.name, c.project.customer.short_name, c.project.customer.type.name, c1, c2, c3,
                c.project.customer.get_priority_display(), c.project.customer.zone.name, c.project.customer.province, c.project.customer.city,
                c.project.customer.address, c.project.customer.get_businessmans_name(),
                str(c.project.customer.registered_capital), c.project.customer.shareholder,
                c.project.customer.product_desc, c.project.customer.notes, str(c.project.customer.timestamp)
            ]
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                writer.writerow([c.encode('utf-8') for c in row])
fobj.close()


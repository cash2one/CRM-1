# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20150923_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='product_desc',
            field=models.TextField(default=b'null', verbose_name='\u5ba2\u6237\u4e1a\u52a1\u6216\u4ea7\u54c1\u63cf\u8ff0'),
            preserve_default=True,
        ),
    ]

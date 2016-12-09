# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_auto_20160121_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapplyprogress',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapplyprogress',
            name='description',
            field=models.TextField(verbose_name='\u63cf\u8ff0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapplyprogress',
            name='progress',
            field=models.IntegerField(default=10, verbose_name='\u8fdb\u5ea6', choices=[(10, 'null'), (11, '\u5206\u6790\u5e08\u62d2\u7edd'), (12, '\u4ea7\u54c1\u7ecf\u7406\u62d2\u7edd'), (13, '\u4ea4\u4ed8\u5de5\u7a0b\u5e08\u62d2\u7edd'), (20, '\u5f85\u5206\u6790\u5e08\u5ba1\u6838'), (30, '\u5f85\u4ea7\u54c1\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapplyprogress',
            name='description',
            field=models.TextField(verbose_name='\u63cf\u8ff0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapplyprogress',
            name='progress',
            field=models.IntegerField(default=1, verbose_name='\u8fdb\u5ea6', choices=[(1, '\u5f85\u6d4b\u8bd5'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210'), (4, '\u9000\u56de')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapplyprogress',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]

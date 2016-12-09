# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20160309_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jsonconfig',
            options={'verbose_name': 'Json\u914d\u7f6e\u4fe1\u606f', 'verbose_name_plural': 'Json\u914d\u7f6e\u4fe1\u606f\u5217\u8868'},
        ),
        migrations.AddField(
            model_name='config',
            name='create_time',
            field=models.DateTimeField(default=datetime.date(2016, 3, 9), verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='config',
            name='description',
            field=models.TextField(default='', verbose_name='\u63cf\u8ff0', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='config',
            name='modify_time',
            field=models.DateTimeField(default=datetime.date(2016, 3, 9), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='create_time',
            field=models.DateTimeField(default=datetime.date(2016, 3, 9), verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='description',
            field=models.TextField(default='', verbose_name='\u63cf\u8ff0', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='modify_time',
            field=models.DateTimeField(default=datetime.date(2016, 3, 9), auto_now=True),
            preserve_default=False,
        ),
    ]

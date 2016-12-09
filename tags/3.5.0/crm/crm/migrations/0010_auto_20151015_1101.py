# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20151015_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapply',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='data_modules',
            field=models.ManyToManyField(to='crm.DataModule', verbose_name='\u6570\u636e\u6a21\u5757', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='contacts',
            field=models.ManyToManyField(to='crm.Contact', verbose_name='\u8054\u7cfb\u4eba', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapply',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True),
            preserve_default=True,
        ),
    ]

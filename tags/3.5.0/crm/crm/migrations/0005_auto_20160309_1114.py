# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('crm', '0004_auto_20160302_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='HNApiProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4ea7\u54c1\u540d\u79f0')),
                ('code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=128, verbose_name='\u7c7b\u522b')),
                ('status', models.BooleanField(default=False, verbose_name='\u72b6\u6001')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u6d77\u7eb3API\u4ea7\u54c1',
                'verbose_name_plural': '\u6d77\u7eb3API\u4ea7\u54c1\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImpConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u540d\u79f0')),
                ('value', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name='\u503c', blank=True)),
            ],
            options={
                'verbose_name': '\u4ea4\u4ed8\u7533\u8bf7\u914d\u7f6e\u4fe1\u606f',
                'verbose_name_plural': '\u4ea4\u4ed8\u7533\u8bf7\u914d\u7f6e\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='br_code',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='nda',
        ),
        migrations.AddField(
            model_name='datamodule',
            name='code',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datamodule',
            name='status',
            field=models.BooleanField(default=False, verbose_name='\u72b6\u6001'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impapply',
            name='operations',
            field=models.ForeignKey(related_name='impapply_operations_set', default=1, verbose_name='\u8fd0\u8425\u7ecf\u7406', to='accounts.UserCredit'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('crm', '0005_auto_20150807_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u540d\u79f0')),
                ('value', models.CharField(max_length=256, verbose_name='\u503c')),
            ],
            options={
                'verbose_name': '\u914d\u7f6e\u4fe1\u606f',
                'verbose_name_plural': '\u914d\u7f6e\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImpApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nda', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7b7e\u7f72\u4fdd\u5bc6\u534f')),
                ('contract', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7b7e\u7f72\u6b63\u5f0f\u5408\u540c')),
                ('account_type', models.IntegerField(default=1, verbose_name='\u8d26\u53f7\u7c7b\u578b', choices=[(1, '\u8bd5\u7528'), (2, '\u6b63\u5f0f')])),
                ('br_code', models.BooleanField(default=False, verbose_name='\u662f\u5426\u90e8\u7f72\u767e\u878d\u4ee3\u7801')),
                ('extra_fields', jsonfield.fields.JSONField(default=dict, verbose_name='\u9644\u52a0\u5b57\u6bb5\u4fe1\u606f')),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('state', models.BooleanField(default=False, verbose_name='\u5b9e\u65bd\u5b8c\u6210')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contact_name', models.CharField(default=b'null', max_length=32, verbose_name='\u8054\u7cfb\u4eba')),
                ('position', models.CharField(max_length=50, verbose_name='\u804c\u4f4d', blank=True)),
                ('tel', models.CharField(max_length=20, verbose_name='\u56fa\u8bdd', blank=True)),
                ('mobile', models.CharField(max_length=20, verbose_name='\u624b\u673a', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='\u90ae\u7bb1', blank=True)),
                ('applyman', models.ForeignKey(related_name='imp_applyman', verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit')),
                ('imp_engineer', models.ForeignKey(related_name='imp', to='accounts.UserCredit')),
                ('product', models.ForeignKey(to='crm.Product')),
                ('project', models.ForeignKey(to='crm.Project')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u5b9e\u65bd\u7533\u8bf7',
                'verbose_name_plural': '\u5b9e\u65bd\u7533\u8bf7\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dts_account', models.CharField(max_length=64, verbose_name='dts\u8d26\u53f7')),
                ('amount_data', models.PositiveIntegerField(verbose_name='\u6d4b\u8bd5\u6570\u636e\u91cf')),
                ('goal', models.TextField(verbose_name='\u672c\u6b21\u6d4b\u8bd5\u76ee\u6807')),
                ('test_fields', models.CharField(max_length=2048, verbose_name='\u5ba2\u6237\u63d0\u4f9b\u7684\u6d4b\u8bd5\u5b57\u6bb5')),
                ('overdue_state', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63d0\u4f9b\u903e\u671f\u72b6\u6001')),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('state', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u5b8c\u6210')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contact_name', models.CharField(default=b'null', max_length=32, verbose_name='\u8054\u7cfb\u4eba')),
                ('position', models.CharField(max_length=50, verbose_name='\u804c\u4f4d', blank=True)),
                ('tel', models.CharField(max_length=20, verbose_name='\u56fa\u8bdd', blank=True)),
                ('mobile', models.CharField(max_length=20, verbose_name='\u624b\u673a', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='\u90ae\u7bb1', blank=True)),
                ('analyser', models.ForeignKey(related_name='analser', to='accounts.UserCredit')),
                ('applyman', models.ForeignKey(related_name='test_applyman', verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit')),
                ('project', models.ForeignKey(to='crm.Project')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u6d4b\u8bd5\u7533\u8bf7',
                'verbose_name_plural': '\u6d4b\u8bd5\u7533\u8bf7\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u6d4b\u8bd5\u7ed3\u679c\u8981\u6c42',
                'verbose_name_plural': '\u6d4b\u8bd5\u7ed3\u679c\u8981\u6c42\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testapply',
            name='test_result',
            field=models.ManyToManyField(to='crm.TestResult', verbose_name='\u6d4b\u8bd5\u7ed3\u679c\u8981\u6c42'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order'], 'verbose_name': '\u4ea7\u54c1', 'verbose_name_plural': '\u4ea7\u54c1\u5217\u8868'},
        ),
        migrations.RemoveField(
            model_name='project',
            name='product',
        ),
        migrations.AddField(
            model_name='customer',
            name='product_desc',
            field=models.TextField(default=b'null', verbose_name='\u4ea7\u54c1\u63cf\u8ff0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='registered_capital',
            field=models.IntegerField(default=0, verbose_name='\u6ce8\u518c\u8d44\u672c'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='shareholder',
            field=models.CharField(default=b'null', max_length=50, verbose_name='\u80a1\u4e1c'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='imp_apply_define',
            field=jsonfield.fields.JSONField(default={b'account': {b'initial': b'', b'required': False, b'type': b'text', b'value': b'', b'label': ''}}, verbose_name='\u5b9e\u65bd\u7533\u8bf7\u5b57\u6bb5\u5b9a\u4e49', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='manager',
            field=models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u4ea7\u54c1\u8d1f\u8d23\u4eba'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='progress',
            name='ptype',
            field=models.IntegerField(default=0, choices=[(0, '\u5e38\u89c4'), (1, '\u6d4b\u8bd5'), (2, '\u5b9e\u65bd')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='implement_progress',
            field=models.IntegerField(default=0, choices=[(0, '\u672a\u7533\u8bf7'), (1, '\u5df2\u7533\u8bf7-\u5f85\u5ba1\u6838'), (2, '\u5df2\u7533\u8bf7-\u5ba1\u6838\u901a\u8fc7'), (3, '\u5b9e\u65bd\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='implemented',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='products',
            field=models.ManyToManyField(to='crm.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='test_progress',
            field=models.IntegerField(default=0, choices=[(0, '\u672a\u7533\u8bf7'), (1, '\u5df2\u7533\u8bf7'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='tested',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=200, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='businessman',
            field=models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u5546\u52a1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=50, verbose_name='\u57ce\u5e02'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u5ba2\u6237\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='notes',
            field=models.TextField(verbose_name='\u5907\u6ce8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='priority',
            field=models.IntegerField(default=2, verbose_name='\u4f18\u5148\u7ea7', choices=[(1, '\u9ad8'), (2, '\u4e2d'), (3, '\u4f4e')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='province',
            field=models.CharField(max_length=50, verbose_name='\u7701\u4efd'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u7c7b\u578b', to='crm.CustomerType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='zone',
            field=models.ForeignKey(verbose_name='\u5927\u533a', to='accounts.Zone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customertype',
            name='name',
            field=models.CharField(max_length=32, verbose_name='\u5ba2\u6237\u7c7b\u578b'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='operator',
            field=models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='businessman',
            field=models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u5546\u52a1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='contacts',
            field=models.ManyToManyField(to='crm.Contact', verbose_name='\u8054\u7cfb\u4eba'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='notes',
            field=models.TextField(verbose_name='\u5907\u6ce8', blank=True),
            preserve_default=True,
        ),
    ]

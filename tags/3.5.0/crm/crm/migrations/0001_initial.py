# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import easy_thumbnails.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160121_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u540d\u79f0')),
                ('value', models.CharField(max_length=255, verbose_name='\u503c')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0', blank=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u914d\u7f6e\u4fe1\u606f',
                'verbose_name_plural': '\u914d\u7f6e\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u59d3\u540d')),
                ('position', models.CharField(max_length=50, verbose_name='\u804c\u4f4d', blank=True)),
                ('tel', models.CharField(max_length=20, verbose_name='\u56fa\u8bdd', blank=True)),
                ('mobile', models.CharField(max_length=20, verbose_name='\u624b\u673a', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='\u90ae\u7bb1', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u8054\u7cfb\u4eba',
                'verbose_name_plural': '\u8054\u7cfb\u4eba\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u5ba2\u6237\u5168\u79f0')),
                ('short_name', models.CharField(max_length=64, verbose_name='\u5ba2\u6237\u7b80\u79f0')),
                ('priority', models.IntegerField(default=3, verbose_name='\u5ba2\u6237\u7ea7\u522b', choices=[(1, '\u516c\u53f8\u7ea7\u91cd\u70b9\u5ba2\u6237'), (2, '\u533a\u57df\u7ea7\u91cd\u70b9\u5ba2\u6237'), (3, '\u975e\u91cd\u70b9\u5ba2\u6237')])),
                ('province', models.CharField(max_length=64, verbose_name='\u7701\u4efd')),
                ('city', models.CharField(max_length=64, verbose_name='\u57ce\u5e02')),
                ('address', models.CharField(max_length=255, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True)),
                ('registered_capital', models.IntegerField(verbose_name='\u6ce8\u518c\u8d44\u672c')),
                ('shareholder', models.CharField(max_length=128, verbose_name='\u80a1\u4e1c')),
                ('product_desc', models.TextField(verbose_name='\u5ba2\u6237\u4e1a\u52a1\u6216\u4ea7\u54c1\u63cf\u8ff0')),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businessman', models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u8ddf\u8fdb\u5546\u52a1')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u5ba2\u6237',
                'verbose_name_plural': '\u5ba2\u6237\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerCategory1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4e00\u7ea7\u7c7b\u76ee\u540d\u79f0')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u5ba2\u6237\u4e00\u7ea7\u7c7b\u76ee',
                'verbose_name_plural': '\u5ba2\u6237\u4e00\u7ea7\u7c7b\u76ee\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerCategory2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4e8c\u7ea7\u7c7b\u76ee\u540d\u79f0')),
                ('order', models.IntegerField(default=0)),
                ('category1', models.ForeignKey(verbose_name='\u5173\u8054\u4e00\u7ea7\u7c7b\u76ee', to='crm.CustomerCategory1')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u5ba2\u6237\u4e8c\u7ea7\u7c7b\u76ee',
                'verbose_name_plural': '\u5ba2\u6237\u4e8c\u7ea7\u7c7b\u76ee\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerCategory3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4e09\u7ea7\u7c7b\u76ee\u540d\u79f0')),
                ('order', models.IntegerField(default=0)),
                ('category2', models.ForeignKey(verbose_name='\u5173\u8054\u4e8c\u7ea7\u7c7b\u76ee', to='crm.CustomerCategory2')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee',
                'verbose_name_plural': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u5ba2\u6237\u7c7b\u578b')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u5ba2\u6237\u7c7b\u578b',
                'verbose_name_plural': '\u5ba2\u6237\u7c7b\u578b\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=128, verbose_name='\u7c7b\u522b')),
                ('status', models.BooleanField(default=False, verbose_name='\u72b6\u6001')),
            ],
            options={
                'verbose_name': '\u6570\u636e\u6a21\u5757',
                'verbose_name_plural': '\u6570\u636e\u6a21\u5757\u5217\u8868',
            },
            bases=(models.Model,),
        ),
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
            name='ImpApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_fields', jsonfield.fields.JSONField(default=dict, verbose_name='\u9644\u52a0\u5b57\u6bb5\u503c', blank=True)),
                ('pic', easy_thumbnails.fields.ThumbnailerImageField(upload_to='email_pic', null=True, verbose_name='\u90ae\u4ef6\u786e\u8ba4\u622a\u56fe', blank=True)),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('progress', models.IntegerField(default=20, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(10, '\u5f85\u63d0\u4ea4'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')])),
                ('state', models.BooleanField(default=False, verbose_name='\u4ea4\u4ed8\u5b8c\u6210')),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('analyser', models.ForeignKey(related_name='impapply_analser_set', verbose_name='\u98ce\u63a7\u7ecf\u7406', blank=True, to='accounts.UserCredit', null=True)),
                ('applicant', models.ForeignKey(related_name='impapply_applicant_set', verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True)),
                ('imp_engineer', models.ForeignKey(related_name='impapply_imp_engineer_set', verbose_name='\u4ea4\u4ed8\u7ecf\u7406', to='accounts.UserCredit')),
                ('operations', models.ForeignKey(related_name='impapply_operations_set', verbose_name='\u8fd0\u8425\u7ecf\u7406', blank=True, to='accounts.UserCredit', null=True)),
            ],
            options={
                'ordering': ['-modify_time'],
                'verbose_name': '\u4ea4\u4ed8\u7533\u8bf7',
                'verbose_name_plural': '\u4ea4\u4ed8\u7533\u8bf7\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImpApplyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(default=10, verbose_name='\u8fdb\u5ea6', choices=[(10, '\u5f85\u63d0\u4ea4'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')])),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0', blank=True)),
                ('operator', models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('imp_apply', models.ForeignKey(to='crm.ImpApply')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u4ea4\u4ed8\u7533\u8bf7\u8fdb\u5ea6',
                'verbose_name_plural': '\u4ea4\u4ed8\u7533\u8bf7\u8fdb\u5ea6\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JsonConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u540d\u79f0')),
                ('value', jsonfield.fields.JSONField(default=dict, verbose_name='\u503c', blank=True)),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0', blank=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': 'Json\u914d\u7f6e\u4fe1\u606f',
                'verbose_name_plural': 'Json\u914d\u7f6e\u4fe1\u606f\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('updatetime', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u6807\u6ce8',
                'verbose_name_plural': '\u6807\u6ce8\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
                ('order', models.IntegerField(default=0, verbose_name='\u987a\u5e8f')),
                ('imp_apply_define', jsonfield.fields.JSONField(default={'account': {'initial': '', 'required': False, 'type': 'text', 'value': '', 'label': ''}}, verbose_name='\u4ea4\u4ed8\u7533\u8bf7form\u5b9a\u4e49', blank=True)),
                ('mark', models.CharField(max_length=32, verbose_name='\u4ee3\u53f7')),
                ('manager', models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u4ea7\u54c1\u8d1f\u8d23\u4eba')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u4ea7\u54c1',
                'verbose_name_plural': '\u4ea7\u54c1\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ptype', models.IntegerField(default=0, choices=[(0, '\u5e38\u89c4'), (1, '\u6d4b\u8bd5'), (2, '\u4ea4\u4ed8')])),
                ('progress', models.IntegerField(default=1, choices=[(1, '\u51c6\u5907'), (2, '\u63a5\u6d3d'), (3, '\u6d4b\u8bd5/\u8bd5\u7528'), (4, '\u8c08\u5224'), (5, '\u4e0a\u7ebf'), (6, '\u552e\u540e')])),
                ('description', models.TextField(blank=True)),
                ('plan', models.TextField(blank=True)),
                ('updatetime', models.DateField(default='1980-01-01')),
                ('operator', models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u8fdb\u5ea6',
                'verbose_name_plural': '\u8fdb\u5ea6\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businessman', models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u5546\u52a1')),
                ('contacts', models.ManyToManyField(to='crm.Contact', verbose_name='\u8054\u7cfb\u4eba', blank=True)),
                ('customer', models.ForeignKey(to='crm.Customer')),
                ('products', models.ManyToManyField(to='crm.Product')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee\u5217\u8868',
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
                ('test_fields', models.CharField(max_length=255, verbose_name='\u5ba2\u6237\u63d0\u4f9b\u7684\u6d4b\u8bd5\u5b57\u6bb5')),
                ('overdue_state', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63d0\u4f9b\u903e\u671f\u72b6\u6001')),
                ('notes', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('state', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u5b8c\u6210')),
                ('progress', models.IntegerField(default=1, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(1, '\u5f85\u6d4b\u8bd5'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210'), (4, '\u9000\u56de')])),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('analyser', models.ForeignKey(related_name='testapply_analser_set', to='accounts.UserCredit')),
                ('applyman', models.ForeignKey(related_name='testapply_applyman_set', verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True)),
                ('project', models.ForeignKey(to='crm.Project')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u6d4b\u8bd5\u7533\u8bf7',
                'verbose_name_plural': '\u6d4b\u8bd5\u7533\u8bf7\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestApplyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(default=1, verbose_name='\u8fdb\u5ea6', choices=[(1, '\u5f85\u6d4b\u8bd5'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210'), (4, '\u9000\u56de')])),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0', blank=True)),
                ('operator', models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('test_apply', models.ForeignKey(to='crm.TestApply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u6d4b\u8bd5\u7533\u8bf7\u8fdb\u5ea6',
                'verbose_name_plural': '\u6d4b\u8bd5\u7533\u8bf7\u8fdb\u5ea6\u5217\u8868',
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
        migrations.AddField(
            model_name='progress',
            name='project',
            field=models.ForeignKey(to='crm.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mark',
            name='progress',
            field=models.OneToOneField(to='crm.Progress'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mark',
            name='usercredit',
            field=models.ForeignKey(to='accounts.UserCredit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impapply',
            name='product',
            field=models.ForeignKey(to='crm.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impapply',
            name='project',
            field=models.ForeignKey(to='crm.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='category1',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u4e00\u7ea7\u7c7b\u76ee', blank=True, to='crm.CustomerCategory1', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='category2',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u4e8c\u7ea7\u7c7b\u76ee', blank=True, to='crm.CustomerCategory2', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='category3',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee', blank=True, to='crm.CustomerCategory3', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u7c7b\u578b', to='crm.CustomerType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='zone',
            field=models.ForeignKey(verbose_name='\u533a\u57df', to='accounts.Zone'),
            preserve_default=True,
        ),
    ]

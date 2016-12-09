# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160121_1348'),
        ('crm', '0012_auto_20151127_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpApplyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(default=10, verbose_name=((10, 'null'), (11, '\u5206\u6790\u5e08\u62d2\u7edd'), (12, '\u4ea7\u54c1\u7ecf\u7406\u62d2\u7edd'), (13, '\u4ea4\u4ed8\u5de5\u7a0b\u5e08\u62d2\u7edd'), (20, '\u5f85\u5206\u6790\u5e08\u5ba1\u6838'), (30, '\u5f85\u4ea7\u54c1\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (50, '\u4ea4\u4ed8\u5b8c\u6210')))),
                ('description', models.TextField(blank=True)),
                ('operator', models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
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
            name='TestApplyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(default=1, verbose_name=((1, '\u5f85\u6d4b\u8bd5'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210'), (4, '\u9000\u56de')))),
                ('description', models.TextField(blank=True)),
                ('operator', models.CharField(max_length=32, verbose_name='\u66f4\u65b0\u4eba')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('test_apply', models.ForeignKey(to='crm.TestApply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u6d4b\u8bd5\u7533\u8bf7\u8fdb\u5ea6',
                'verbose_name_plural': '\u6d4b\u8bd5\u7533\u8bf7\u8fdb\u5ea6\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='impapply',
            options={'ordering': ['-modify_time'], 'verbose_name': '\u4ea4\u4ed8\u7533\u8bf7', 'verbose_name_plural': '\u4ea4\u4ed8\u7533\u8bf7\u5217\u8868'},
        ),
        migrations.RenameField(
            model_name='impapply',
            old_name='timestamp',
            new_name='create_time',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='applyman',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='data_modules',
        ),
        migrations.RemoveField(
            model_name='project',
            name='implement_progress',
        ),
        migrations.RemoveField(
            model_name='project',
            name='implemented',
        ),
        migrations.RemoveField(
            model_name='project',
            name='test_progress',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tested',
        ),
        migrations.AddField(
            model_name='customer',
            name='short_name',
            field=models.CharField(default='', max_length=64, verbose_name='\u5ba2\u6237\u7b80\u79f0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impapply',
            name='analyser',
            field=models.ForeignKey(related_name='impapply_analser_set', default=1, verbose_name='\u5206\u6790\u5e08', to='accounts.UserCredit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impapply',
            name='applicant',
            field=models.ForeignKey(related_name='impapply_applicant_set', default=1, verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impapply',
            name='modify_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 21, 13, 48, 28, 171322), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impapply',
            name='progress',
            field=models.IntegerField(default=20, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(10, 'null'), (11, '\u5206\u6790\u5e08\u62d2\u7edd'), (12, '\u4ea7\u54c1\u7ecf\u7406\u62d2\u7edd'), (13, '\u4ea4\u4ed8\u5de5\u7a0b\u5e08\u62d2\u7edd'), (20, '\u5f85\u5206\u6790\u5e08\u5ba1\u6838'), (30, '\u5f85\u4ea7\u54c1\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='mark',
            field=models.CharField(default='', max_length=32, verbose_name='\u4ee3\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testapply',
            name='progress',
            field=models.IntegerField(default=1, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(1, '\u5f85\u6d4b\u8bd5'), (2, '\u6d4b\u8bd5\u4e2d'), (3, '\u6d4b\u8bd5\u5b8c\u6210'), (4, '\u9000\u56de')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='config',
            name='value',
            field=models.CharField(max_length=255, verbose_name='\u503c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=255, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='businessman',
            field=models.ManyToManyField(to='accounts.UserCredit', verbose_name='\u8ddf\u8fdb\u5546\u52a1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=64, verbose_name='\u57ce\u5e02'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=128, verbose_name='\u5ba2\u6237\u5168\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='province',
            field=models.CharField(max_length=64, verbose_name='\u7701\u4efd'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='shareholder',
            field=models.CharField(default='null', max_length=128, verbose_name='\u80a1\u4e1c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(verbose_name='\u7c7b\u578b', to='crm.CustomerType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='zone',
            field=models.ForeignKey(verbose_name='\u533a\u57df', to='accounts.Zone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='br_code',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u90e8\u7f72\u767e\u878d\u4ee3\u7801', choices=[(0, '\u5426'), (1, '\u662f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='contract',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u5df2\u7b7e\u7f72\u6b63\u5f0f\u5408\u540c', choices=[(0, '\u5426'), (1, '\u662f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='extra_fields',
            field=jsonfield.fields.JSONField(default=dict, verbose_name='\u9644\u52a0\u5b57\u6bb5\u503c', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='imp_engineer',
            field=models.ForeignKey(related_name='impapply_imp_engineer_set', verbose_name='\u4ea4\u4ed8\u5de5\u7a0b\u5e08', to='accounts.UserCredit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='nda',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u5df2\u7b7e\u7f72\u4fdd\u5bc6\u534f', choices=[(0, '\u5426'), (1, '\u662f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.IntegerField(default=0, verbose_name='\u987a\u5e8f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapply',
            name='analyser',
            field=models.ForeignKey(related_name='testapply_analser_set', to='accounts.UserCredit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapply',
            name='applyman',
            field=models.ForeignKey(related_name='testapply_applyman_set', verbose_name='\u7533\u8bf7\u4eba', to='accounts.UserCredit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testapply',
            name='test_fields',
            field=models.CharField(max_length=255, verbose_name='\u5ba2\u6237\u63d0\u4f9b\u7684\u6d4b\u8bd5\u5b57\u6bb5'),
            preserve_default=True,
        ),
    ]

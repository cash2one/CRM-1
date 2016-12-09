# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCategory1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4e00\u7ea7\u7c7b\u76ee\u540d\u79f0')),
            ],
            options={
                'ordering': ['id'],
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
                ('category1', models.ForeignKey(verbose_name='\u5173\u8054\u4e00\u7ea7\u7c7b\u76ee', to='crm.CustomerCategory1')),
            ],
            options={
                'ordering': ['id'],
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
                ('category2', models.ForeignKey(verbose_name='\u5173\u8054\u4e8c\u7ea7\u7c7b\u76ee', to='crm.CustomerCategory2')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee',
                'verbose_name_plural': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='project',
            name='priority',
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
        migrations.AlterField(
            model_name='customer',
            name='priority',
            field=models.IntegerField(default=2, verbose_name='\u5ba2\u6237\u7ea7\u522b', choices=[(1, '\u516c\u53f8\u7ea7\u91cd\u70b9\u5ba2\u6237'), (2, '\u533a\u57df\u7ea7\u91cd\u70b9\u5ba2\u6237'), (3, '\u975e\u91cd\u70b9\u5ba2\u6237')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='product_desc',
            field=models.TextField(verbose_name='\u5ba2\u6237\u4e1a\u52a1\u6216\u4ea7\u54c1\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_capital',
            field=models.IntegerField(verbose_name='\u6ce8\u518c\u8d44\u672c'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='shareholder',
            field=models.CharField(max_length=128, verbose_name='\u80a1\u4e1c'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237\u7c7b\u578b', to='crm.CustomerType'),
        ),
        migrations.AlterField(
            model_name='impapply',
            name='analyser',
            field=models.ForeignKey(related_name='impapply_analser_set', verbose_name='\u98ce\u63a7\u7ecf\u7406', to='accounts.UserCredit'),
        ),
        migrations.AlterField(
            model_name='impapply',
            name='imp_engineer',
            field=models.ForeignKey(related_name='impapply_imp_engineer_set', verbose_name='\u4ea4\u4ed8\u7ecf\u7406', to='accounts.UserCredit'),
        ),
        migrations.AlterField(
            model_name='impapply',
            name='progress',
            field=models.IntegerField(default=20, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(10, 'null'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
        ),
        migrations.AlterField(
            model_name='impapplyprogress',
            name='progress',
            field=models.IntegerField(default=10, verbose_name='\u8fdb\u5ea6', choices=[(10, 'null'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20150924_0431'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('category', models.CharField(max_length=128, verbose_name='\u7c7b\u522b')),
            ],
            options={
                'verbose_name': '\u6570\u636e\u6a21\u5757',
                'verbose_name_plural': '\u6570\u636e\u6a21\u5757\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='impapply',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u4ea4\u4ed8\u7533\u8bf7', 'verbose_name_plural': '\u4ea4\u4ed8\u7533\u8bf7\u5217\u8868'},
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='email',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='position',
        ),
        migrations.RemoveField(
            model_name='impapply',
            name='tel',
        ),
        migrations.RemoveField(
            model_name='testapply',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='testapply',
            name='email',
        ),
        migrations.RemoveField(
            model_name='testapply',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='testapply',
            name='position',
        ),
        migrations.RemoveField(
            model_name='testapply',
            name='tel',
        ),
        migrations.AddField(
            model_name='impapply',
            name='contact',
            field=models.ForeignKey(verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impapply',
            name='data_modules',
            field=models.ManyToManyField(to='crm.DataModule', verbose_name='\u6570\u636e\u6a21\u5757'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testapply',
            name='contact',
            field=models.ForeignKey(verbose_name='\u8054\u7cfb\u4eba', blank=True, to='crm.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='\u90ae\u7bb1', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(max_length=20, verbose_name='\u624b\u673a', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=32, verbose_name='\u59d3\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='position',
            field=models.CharField(max_length=50, verbose_name='\u804c\u4f4d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='tel',
            field=models.CharField(max_length=20, verbose_name='\u56fa\u8bdd', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='state',
            field=models.BooleanField(default=False, verbose_name='\u4ea4\u4ed8\u5b8c\u6210'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='imp_apply_define',
            field=jsonfield.fields.JSONField(default={b'account': {b'initial': b'', b'required': False, b'type': b'text', b'value': b'', b'label': ''}}, verbose_name='\u4ea4\u4ed8\u7533\u8bf7form\u5b9a\u4e49', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='ptype',
            field=models.IntegerField(default=0, choices=[(0, '\u5e38\u89c4'), (1, '\u6d4b\u8bd5'), (2, '\u4ea4\u4ed8')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='updatetime',
            field=models.DateField(default=b'1980-01-01'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='implement_progress',
            field=models.IntegerField(default=0, choices=[(0, '\u672a\u7533\u8bf7'), (1, '\u5df2\u7533\u8bf7-\u5f85\u5ba1\u6838'), (2, '\u5df2\u7533\u8bf7-\u5ba1\u6838\u901a\u8fc7'), (3, '\u4ea4\u4ed8\u5b8c\u6210')]),
            preserve_default=True,
        ),
    ]

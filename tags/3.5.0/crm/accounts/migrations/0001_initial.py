# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['role'],
                'verbose_name': '\u89d2\u8272',
                'verbose_name_plural': '\u89d2\u8272\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.IntegerField(default=0, verbose_name='\u6743\u9650\u7b49\u7ea7', choices=[(0, '\u666e\u901a'), (1, '\u9ad8\u7ea7'), (2, '\u8d85\u7ea7')])),
                ('test_flag', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u8d26\u53f7\u6807\u8bb0')),
                ('role', models.ForeignKey(to='accounts.Role')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u767e\u878d\u7528\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u5927\u533a',
                'verbose_name_plural': '\u5927\u533a\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='usercredit',
            name='zone',
            field=models.ForeignKey(to='accounts.Zone'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('crm', '0003_auto_20150624_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('updatetime', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('progress', models.OneToOneField(to='crm.Progress')),
                ('usercredit', models.ForeignKey(to='accounts.UserCredit')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': '\u6807\u6ce8',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u8fdb\u5ea6'},
        ),
    ]

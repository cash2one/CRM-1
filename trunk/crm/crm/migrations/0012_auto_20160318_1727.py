# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_auto_20160316_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testapply',
            options={'ordering': ['-create_time'], 'verbose_name': '\u6d4b\u8bd5\u7533\u8bf7', 'verbose_name_plural': '\u6d4b\u8bd5\u7533\u8bf7\u5217\u8868'},
        ),
        migrations.RenameField(
            model_name='testapply',
            old_name='timestamp',
            new_name='create_time',
        ),
        migrations.AddField(
            model_name='testapply',
            name='modify_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 18, 17, 27, 37, 710993), auto_now=True),
            preserve_default=False,
        ),
    ]

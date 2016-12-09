# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20150806_0737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['name'], 'verbose_name': '\u8054\u7cfb\u4eba', 'verbose_name_plural': '\u8054\u7cfb\u4eba\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u5ba2\u6237', 'verbose_name_plural': '\u5ba2\u6237\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='mark',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u6807\u6ce8', 'verbose_name_plural': '\u6807\u6ce8\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u8fdb\u5ea6', 'verbose_name_plural': '\u8fdb\u5ea6\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-timestamp'], 'verbose_name': '\u9879\u76ee', 'verbose_name_plural': '\u9879\u76ee\u5217\u8868'},
        ),
    ]

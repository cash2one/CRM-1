# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_remove_project_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customertype',
            options={'ordering': ['order'], 'verbose_name': '\u5ba2\u6237\u7c7b\u578b', 'verbose_name_plural': '\u5ba2\u6237\u7c7b\u578b\u5217\u8868'},
        ),
        migrations.AlterField(
            model_name='progress',
            name='progress',
            field=models.IntegerField(default=1, choices=[(1, '\u51c6\u5907'), (2, '\u63a5\u6d3d'), (3, '\u6d4b\u8bd5/\u8bd5\u7528'), (4, '\u8c08\u5224'), (5, '\u4e0a\u7ebf'), (6, '\u552e\u540e')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.IntegerField(default=2, choices=[(1, '\u9ad8'), (2, '\u4e2d'), (3, '\u4f4e')]),
            preserve_default=True,
        ),
    ]

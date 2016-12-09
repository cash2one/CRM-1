# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_product_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progress',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'updatetime', 'verbose_name': '\u8fdb\u5ea6'},
        ),
    ]

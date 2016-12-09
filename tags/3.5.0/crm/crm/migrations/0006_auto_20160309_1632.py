# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20160309_1114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImpConfig',
            new_name='JsonConfig',
        ),
    ]

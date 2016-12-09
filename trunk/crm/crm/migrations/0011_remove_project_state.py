# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_auto_20151015_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='state',
        ),
    ]

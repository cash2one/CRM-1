# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20150921_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapply',
            name='extra_fields',
            field=jsonfield.fields.JSONField(default=dict, verbose_name='\u9644\u52a0\u5b57\u6bb5\u4fe1\u606f', blank=True),
            preserve_default=True,
        ),
    ]

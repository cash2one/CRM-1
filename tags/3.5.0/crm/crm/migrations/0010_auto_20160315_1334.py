# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20160315_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapply',
            name='pic',
            field=models.ImageField(upload_to='media', null=True, verbose_name='\u90ae\u4ef6\u786e\u8ba4\u622a\u56fe', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20160315_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapply',
            name='pic',
            field=models.ImageField(default='', upload_to='/media/', verbose_name='\u90ae\u4ef6\u786e\u8ba4\u622a\u56fe', blank=True),
            preserve_default=False,
        ),
    ]

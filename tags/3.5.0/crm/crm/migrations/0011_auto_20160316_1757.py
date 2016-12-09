# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_auto_20160315_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impapply',
            name='pic',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='email_pic', null=True, verbose_name='\u90ae\u4ef6\u786e\u8ba4\u622a\u56fe', blank=True),
            preserve_default=True,
        ),
    ]

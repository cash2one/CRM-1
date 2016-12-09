# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercredit',
            name='test_flag',
            field=models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u8d26\u53f7\u6807\u8bb0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercredit',
            name='privilege',
            field=models.IntegerField(default=0, verbose_name='\u6743\u9650\u7b49\u7ea7', choices=[(0, '\u666e\u901a'), (1, '\u9ad8\u7ea7'), (2, '\u8d85\u7ea7')]),
            preserve_default=True,
        ),
    ]

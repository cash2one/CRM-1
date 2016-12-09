# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151127_0735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zone',
            options={'ordering': ['order'], 'verbose_name': '\u5927\u533a', 'verbose_name_plural': '\u5927\u533a\u5217\u8868'},
        ),
        migrations.AddField(
            model_name='zone',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20160223_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customercategory1',
            options={'ordering': ['order'], 'verbose_name': '\u5ba2\u6237\u4e00\u7ea7\u7c7b\u76ee', 'verbose_name_plural': '\u5ba2\u6237\u4e00\u7ea7\u7c7b\u76ee\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='customercategory2',
            options={'ordering': ['order'], 'verbose_name': '\u5ba2\u6237\u4e8c\u7ea7\u7c7b\u76ee', 'verbose_name_plural': '\u5ba2\u6237\u4e8c\u7ea7\u7c7b\u76ee\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='customercategory3',
            options={'ordering': ['order'], 'verbose_name': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee', 'verbose_name_plural': '\u5ba2\u6237\u4e09\u7ea7\u7c7b\u76ee\u5217\u8868'},
        ),
        migrations.AddField(
            model_name='customercategory1',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customercategory2',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customercategory3',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

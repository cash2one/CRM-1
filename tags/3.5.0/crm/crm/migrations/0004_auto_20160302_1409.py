# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20160225_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='priority',
            field=models.IntegerField(default=3, verbose_name='\u5ba2\u6237\u7ea7\u522b', choices=[(1, '\u516c\u53f8\u7ea7\u91cd\u70b9\u5ba2\u6237'), (2, '\u533a\u57df\u7ea7\u91cd\u70b9\u5ba2\u6237'), (3, '\u975e\u91cd\u70b9\u5ba2\u6237')]),
        ),
    ]

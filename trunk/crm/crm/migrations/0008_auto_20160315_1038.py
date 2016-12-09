# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20160309_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='impapply',
            name='pic',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='\u90ae\u4ef6\u786e\u8ba4\u622a\u56fe', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapply',
            name='progress',
            field=models.IntegerField(default=20, verbose_name='\u5f53\u524d\u9636\u6bb5', choices=[(10, '\u5f85\u63d0\u4ea4'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impapplyprogress',
            name='progress',
            field=models.IntegerField(default=10, verbose_name='\u8fdb\u5ea6', choices=[(10, '\u5f85\u63d0\u4ea4'), (11, '\u98ce\u63a7\u7ecf\u7406\u9000\u56de'), (12, '\u8fd0\u8425\u7ecf\u7406\u9000\u56de'), (13, '\u4ea4\u4ed8\u7ecf\u7406\u9000\u56de'), (20, '\u5f85\u98ce\u63a7\u7ecf\u7406\u5ba1\u6838'), (30, '\u5f85\u8fd0\u8425\u7ecf\u7406\u5ba1\u6838'), (40, '\u5f85\u4ea4\u4ed8'), (45, '\u4ea4\u4ed8\u4e2d'), (50, '\u4ea4\u4ed8\u5b8c\u6210')]),
            preserve_default=True,
        ),
    ]

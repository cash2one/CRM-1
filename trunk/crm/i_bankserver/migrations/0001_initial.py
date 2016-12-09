# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BCustomConfiguration',
            fields=[
            ],
            options={
                'db_table': 'B_CUSTOM_CONFIGURATION',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BDatasource',
            fields=[
            ],
            options={
                'db_table': 'B_DATASOURCE',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BMapping',
            fields=[
            ],
            options={
                'db_table': 'B_MAPPING',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BMerchant',
            fields=[
            ],
            options={
                'db_table': 'B_MERCHANT',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BProduct',
            fields=[
            ],
            options={
                'db_table': 'B_PRODUCT',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BRuleDepends',
            fields=[
            ],
            options={
                'db_table': 'B_RULE_DEPENDS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BScoreDepends',
            fields=[
            ],
            options={
                'db_table': 'B_SCORE_DEPENDS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BUserCust',
            fields=[
            ],
            options={
                'db_table': 'B_USER_CUST',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BUserProduct',
            fields=[
            ],
            options={
                'db_table': 'B_USER_PRODUCT',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]

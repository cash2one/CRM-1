# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountsRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'accounts_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsUsercredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.IntegerField()),
                ('test_flag', models.IntegerField()),
                ('role_id', models.IntegerField()),
                ('user_id', models.IntegerField(unique=True)),
                ('zone_id', models.IntegerField()),
                ('cid', models.CharField(max_length=128)),
                ('devicetoken', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'accounts_usercredit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'accounts_zone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.IntegerField()),
                ('permission_id', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('content_type_id', models.IntegerField()),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthtokenToken',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('user_id', models.IntegerField(unique=True)),
            ],
            options={
                'db_table': 'authtoken_token',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('group_id', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('permission_id', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CeleryTaskmeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(unique=True, max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('result', models.TextField(null=True, blank=True)),
                ('date_done', models.DateTimeField()),
                ('traceback', models.TextField(null=True, blank=True)),
                ('hidden', models.IntegerField()),
                ('meta', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'celery_taskmeta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CeleryTasksetmeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taskset_id', models.CharField(unique=True, max_length=255)),
                ('result', models.TextField()),
                ('date_done', models.DateTimeField()),
                ('hidden', models.IntegerField()),
            ],
            options={
                'db_table': 'celery_tasksetmeta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('modify_time', models.DateTimeField()),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'crm_config',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('position', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=75)),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=64)),
                ('type_id', models.IntegerField()),
                ('category1_id', models.IntegerField(null=True, blank=True)),
                ('category2_id', models.IntegerField(null=True, blank=True)),
                ('category3_id', models.IntegerField(null=True, blank=True)),
                ('priority', models.IntegerField()),
                ('zone_id', models.IntegerField()),
                ('province', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=255)),
                ('registered_capital', models.IntegerField()),
                ('shareholder', models.CharField(max_length=128)),
                ('product_desc', models.TextField()),
                ('notes', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomerBusinessman',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_id', models.IntegerField()),
                ('usercredit_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customer_businessman',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomercategory1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customercategory1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomercategory2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('category1_id', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customercategory2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomercategory3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('category2_id', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customercategory3',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmCustomertype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_customertype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmDatamodule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=128)),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_datamodule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmHnapiproduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=128)),
                ('status', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_hnapiproduct',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmImpapply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_id', models.IntegerField()),
                ('analyser_id', models.IntegerField(null=True, blank=True)),
                ('operations_id', models.IntegerField(null=True, blank=True)),
                ('imp_engineer_id', models.IntegerField()),
                ('project_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('extra_fields', models.TextField()),
                ('contact_id', models.IntegerField(null=True, blank=True)),
                ('pic', models.CharField(max_length=100, null=True, blank=True)),
                ('notes', models.TextField()),
                ('progress', models.IntegerField()),
                ('state', models.IntegerField()),
                ('modify_time', models.DateTimeField()),
                ('create_time', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_impapply',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmImpapplyprogress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imp_apply_id', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('description', models.TextField()),
                ('operator', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_impapplyprogress',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmJsonconfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('value', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('description', models.TextField()),
                ('modify_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'crm_jsonconfig',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usercredit_id', models.IntegerField()),
                ('progress_id', models.IntegerField(unique=True)),
                ('content', models.TextField()),
                ('updatetime', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'crm_mark',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('imp_apply_define', models.TextField()),
                ('mark', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'crm_product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProductManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField()),
                ('usercredit_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_product_manager',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ptype', models.IntegerField()),
                ('project_id', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('description', models.TextField()),
                ('plan', models.TextField()),
                ('updatetime', models.DateField()),
                ('operator', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'crm_progress',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('customer_id', models.IntegerField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProjectBusinessman',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.IntegerField()),
                ('usercredit_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_project_businessman',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProjectContacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.IntegerField()),
                ('contact_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_project_contacts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmProjectProducts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_project_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmTestapply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applyman_id', models.IntegerField()),
                ('project_id', models.IntegerField()),
                ('dts_account', models.CharField(max_length=64)),
                ('analyser_id', models.IntegerField()),
                ('amount_data', models.IntegerField()),
                ('goal', models.TextField()),
                ('test_fields', models.CharField(max_length=255)),
                ('overdue_state', models.IntegerField()),
                ('notes', models.TextField()),
                ('state', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('modify_time', models.DateTimeField()),
                ('create_time', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
                ('contact_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'crm_testapply',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmTestapplyprogress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_apply_id', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('description', models.TextField()),
                ('operator', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_testapplyprogress',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmTestapplyTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testapply_id', models.IntegerField()),
                ('testresult_id', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_testapply_test_result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CrmTestresult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField()),
            ],
            options={
                'db_table': 'crm_testresult',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
                ('content_type_id', models.IntegerField(null=True, blank=True)),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryCrontabschedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minute', models.CharField(max_length=64)),
                ('hour', models.CharField(max_length=64)),
                ('day_of_week', models.CharField(max_length=64)),
                ('day_of_month', models.CharField(max_length=64)),
                ('month_of_year', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'djcelery_crontabschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryIntervalschedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('every', models.IntegerField()),
                ('period', models.CharField(max_length=24)),
            ],
            options={
                'db_table': 'djcelery_intervalschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryPeriodictask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('task', models.CharField(max_length=200)),
                ('args', models.TextField()),
                ('kwargs', models.TextField()),
                ('queue', models.CharField(max_length=200, null=True, blank=True)),
                ('exchange', models.CharField(max_length=200, null=True, blank=True)),
                ('routing_key', models.CharField(max_length=200, null=True, blank=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('enabled', models.IntegerField()),
                ('last_run_at', models.DateTimeField(null=True, blank=True)),
                ('total_run_count', models.IntegerField()),
                ('date_changed', models.DateTimeField()),
                ('description', models.TextField()),
                ('crontab_id', models.IntegerField(null=True, blank=True)),
                ('interval_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'djcelery_periodictask',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryPeriodictasks',
            fields=[
                ('ident', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('last_update', models.DateTimeField()),
            ],
            options={
                'db_table': 'djcelery_periodictasks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryTaskstate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=64)),
                ('task_id', models.CharField(unique=True, max_length=36)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('tstamp', models.DateTimeField()),
                ('args', models.TextField(null=True, blank=True)),
                ('kwargs', models.TextField(null=True, blank=True)),
                ('eta', models.DateTimeField(null=True, blank=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('result', models.TextField(null=True, blank=True)),
                ('traceback', models.TextField(null=True, blank=True)),
                ('runtime', models.FloatField(null=True, blank=True)),
                ('retries', models.IntegerField()),
                ('hidden', models.IntegerField()),
                ('worker_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'djcelery_taskstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryWorkerstate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=255)),
                ('last_heartbeat', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'djcelery_workerstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjkombuMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visible', models.IntegerField()),
                ('sent_at', models.DateTimeField(null=True, blank=True)),
                ('payload', models.TextField()),
                ('queue_id', models.IntegerField()),
            ],
            options={
                'db_table': 'djkombu_message',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjkombuQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
            options={
                'db_table': 'djkombu_queue',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EasyThumbnailsSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('storage_hash', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=255)),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'easy_thumbnails_source',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EasyThumbnailsThumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('storage_hash', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=255)),
                ('modified', models.DateTimeField()),
                ('source_id', models.IntegerField()),
            ],
            options={
                'db_table': 'easy_thumbnails_thumbnail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EasyThumbnailsThumbnaildimensions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thumbnail_id', models.IntegerField(unique=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'easy_thumbnails_thumbnaildimensions',
                'managed': False,
            },
        ),
    ]

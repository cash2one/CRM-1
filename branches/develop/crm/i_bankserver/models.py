# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import collections
import logging
from django.db import models
from django.db.models import  Q
from crm.models import JsonConfig
from crm.common import list_group
ERR_LOG = logging.getLogger('crm_error')

class BCustomConfiguration(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    custom_code = models.CharField(db_column='CUSTOM_CODE', max_length=200, blank=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    custom_info = models.CharField(db_column='CUSTOM_INFO', max_length=200, blank=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_CUSTOM_CONFIGURATION'


class BDatasource(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    api_code = models.CharField(db_column='API_CODE', max_length=20, blank=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=200, blank=True)  # Field name made lowercase.
    db_port = models.CharField(db_column='DB_PORT', max_length=20, blank=True)  # Field name made lowercase.
    db_address = models.CharField(db_column='DB_ADDRESS', max_length=500, blank=True)  # Field name made lowercase.
    db_username = models.CharField(db_column='DB_USERNAME', max_length=200, blank=True)  # Field name made lowercase.
    db_password = models.CharField(db_column='DB_PASSWORD', max_length=200, blank=True)  # Field name made lowercase.
    db_parameter = models.CharField(db_column='DB_PARAMETER', max_length=200, blank=True)  # Field name made lowercase.
    db_driver = models.CharField(db_column='DB_DRIVER', max_length=200, blank=True)  # Field name made lowercase.
    db_type = models.IntegerField(db_column='DB_TYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_DATASOURCE'


class BMapping(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=255, blank=True)  # Field name made lowercase.
    mapping_code = models.CharField(db_column='MAPPING_CODE', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_MAPPING'


class BMerchant(models.Model):
    user_id = models.IntegerField(db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    merchant_name = models.CharField(db_column='MERCHANT_NAME', max_length=200, blank=True)  # Field name made lowercase.
    short_name = models.CharField(db_column='SHORT_NAME', max_length=20, blank=True)  # Field name made lowercase.
    rebate_market = models.DecimalField(db_column='REBATE_MARKET', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rebate_data = models.DecimalField(db_column='REBATE_DATA', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    user_desc = models.CharField(db_column='USER_DESC', max_length=500, blank=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.
    api_code = models.CharField(db_column='API_CODE', unique=True, max_length=200, blank=True)  # Field name made lowercase.
    limit_day_time = models.IntegerField(db_column='LIMIT_DAY_TIME')  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.
    is_charging = models.IntegerField(db_column='IS_CHARGING', blank=True, null=True)  # Field name made lowercase.
    is_admin = models.IntegerField(db_column='IS_ADMIN', blank=True, null=True)  # Field name made lowercase.
    is_check = models.IntegerField(db_column='IS_CHECK')  # Field name made lowercase.
    user_type = models.CharField(db_column='USER_TYPE', max_length=20, blank=True)  # Field name made lowercase.
    custom_request = models.CharField(db_column='CUSTOM_REQUEST', max_length=200, blank=True)  # Field name made lowercase.
    custom_response = models.CharField(db_column='CUSTOM_RESPONSE', max_length=200, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_MERCHANT'


class BProduct(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=200, blank=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=200, blank=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=200, blank=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME')  # Field name made lowercase.
    order = models.IntegerField(db_column='ORDER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_PRODUCT'

    @classmethod
    def get_types(cls):
        """获取所有的分类"""
        type_list = cls.objects.filter(status=1).all().order_by("code").values_list('type', flat=True)
        return list(set(type_list))
    @classmethod
    def get_data_dict(cls):
        """用OrderedDict存储数据"""
        type_list = cls.get_types()
        enabled_modules = JsonConfig.objects.filter(name='enabled-modules').first()
        if enabled_modules:
            obj_set = cls.objects.filter(status=1, code__in=enabled_modules.value).all().order_by("code")
        else:
            obj_set = cls.objects.all().order_by("code")
        data_dict = collections.OrderedDict()
        for t in type_list:
            data = obj_set.filter(type=t).all()
            if t == "api" or t == "ter":
                data = obj_set.filter(Q(type="api") | Q(type="ter")).all()
                data_dict["ter"] = list_group(data, 2)
            data_dict[t] = list_group(data, 2)
        try:
            data_dict.pop("api")
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        return data_dict

    def __unicode__(self):
        return self.name


class BRuleDepends(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=20, blank=True)  # Field name made lowercase.
    request_code = models.CharField(db_column='REQUEST_CODE', max_length=500, blank=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_RULE_DEPENDS'


class BScoreDepends(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=20, blank=True)  # Field name made lowercase.
    request_code = models.CharField(db_column='REQUEST_CODE', max_length=500, blank=True)  # Field name made lowercase.
    create_time = models.BigIntegerField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.
    update_time = models.BigIntegerField(db_column='UPDATE_TIME', blank=True, null=True)  # Field name made lowercase.
    file_url = models.CharField(db_column='FILE_URL', max_length=200, blank=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_SCORE_DEPENDS'


class BUserCust(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    api_code = models.CharField(db_column='API_CODE', max_length=200, blank=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=200, blank=True)  # Field name made lowercase.
    cust_mapping = models.CharField(db_column='CUST_MAPPING', max_length=200, blank=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_USER_CUST'


class BUserProduct(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    api_code = models.CharField(db_column='API_CODE', max_length=200, blank=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=200, blank=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B_USER_PRODUCT'

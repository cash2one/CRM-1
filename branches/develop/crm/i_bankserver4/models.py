# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

import collections
import logging
from django.db import models
from django.db.models import  Q
from crm.models import JsonConfig
from crm.common import list_group
ERR_LOG = logging.getLogger('crm_error')


class BCustomConfiguration(models.Model):
    custom_code = models.CharField(max_length=200, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    custom_info = models.CharField(max_length=200, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'B_CUSTOM_CONFIGURATION'


class BMerchant4(models.Model):
    status = models.IntegerField()
    api_code = models.CharField(unique=True, max_length=200, blank=True, null=True)
    limit_day_time = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)
    is_charging = models.IntegerField(blank=True, null=True)
    is_apply_loan = models.IntegerField(blank=True, null=True)
    is_check = models.IntegerField()
    user_type = models.IntegerField(blank=True, null=True)
    custom_request = models.CharField(max_length=200)
    custom_response = models.CharField(max_length=200)
    meal = models.TextField()

    class Meta:
        managed = False
        db_table = 'B_MERCHANT_4'


class BProduct(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    order = models.IntegerField(blank=True, null=True)
    api_v = models.CharField(max_length=100, blank=True, null=True)
    data_v = models.CharField(max_length=100, blank=True, null=True)
    service_name = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)

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


class BScoreDepends(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    request_code = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)
    update_time = models.BigIntegerField(blank=True, null=True)
    file_url = models.CharField(max_length=200, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'B_SCORE_DEPENDS'


class BUserCust(models.Model):
    api_code = models.CharField(max_length=200, blank=True, null=True)
    product_code = models.CharField(max_length=200, blank=True, null=True)
    cust_mapping = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'B_USER_CUST'

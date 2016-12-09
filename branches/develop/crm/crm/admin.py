# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    CustomerType, Product, Customer, Contact, Project, Progress, Mark, TestApply, TestApplyProgress,
    TestResult, ImpApply, ImpApplyProgress, Config, DataModule, CustomerCategory1, CustomerCategory2,
    CustomerCategory3, HNApiProduct, JsonConfig
)


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(CustomerCategory1)
class CustomerCategory1Admin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(CustomerCategory2)
class CustomerCategory2Admin(admin.ModelAdmin):
    list_display = ('name', 'get_category1', 'order')
    ordering = ('category1', 'order')

    def get_category1(self, obj):
        return obj.category1.name
    get_category1.short_description = u'宿主一级类目'


@admin.register(CustomerCategory3)
class CustomerCategory3Admin(admin.ModelAdmin):
    list_display = ('name', 'get_category2', 'order')
    ordering = ('category2', 'order')

    def get_category2(self, obj):
        return obj.category2.name
    get_category2.short_description = u'宿主二级类目'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'p_manager')
    filter_horizontal = ('manager',)

    def p_manager(self, obj):
        return ','.join([usercredit.user.first_name for usercredit in obj.manager.all()])
    p_manager.short_description = u'产品负责人'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type_name', 'get_zone_name', 'city')
    search_fields = ('name',)

    def get_type_name(self, obj):
        return obj.type.name
    get_type_name.short_description = u'类型'

    def get_zone_name(self, obj):
        return obj.zone.name
    get_zone_name.short_description = u'大区'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_customer_name', 'get_products_name')
    search_fields = ('name',)

    def get_customer_name(self, obj):
        return obj.customer.name
    get_customer_name.short_description = u'客户'

    def get_products_name(self, obj):
        return ','.join([p.name for p in obj.products.all()])
    get_products_name.short_description = u'产品'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'mobile')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('get_project_name', 'get_progress_display', 'operator')

    def get_project_name(self, obj):
        return obj.project.name
    get_project_name.short_description = u'项目'


@admin.register(TestApply)
class TestApplyAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'analyser', 'create_time')

    def project_name(self, obj):
        return obj.project.name
    project_name.short_description = u'项目'


@admin.register(TestApplyProgress)
class TestApplyProgressAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'get_progress_display', 'description', 'operator', 'timestamp')
    def project_name(self, obj):
        return obj.test_apply.project.name
    project_name.short_description = u'项目'


@admin.register(TestResult)
class TestResult(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(ImpApply)
class ImpApplyAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'product', 'applicant', 'imp_engineer', 'state', 'create_time',"contact")

    def project_name(self, obj):
        return obj.project.name
    project_name.short_description = u'项目'


@admin.register(ImpApplyProgress)
class ImpApplyProgressAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'product_name', 'get_progress_display', 'description', 'operator', 'create_time')

    def project_name(self, obj):
        return obj.imp_apply.project.name
    project_name.short_description = u'项目'

    def product_name(self, obj):
        return obj.imp_apply.product.name
    product_name.short_description = u'产品'


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('get_progress', 'get_user_name', 'updatetime')

    def get_progress(self, obj):
        return obj.progress.get_progress_display()
    get_progress.short_description = u'进度'

    def get_user_name(self, obj):
        return obj.usercredit.user.first_name
    get_user_name.short_description = u'用户'


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


@admin.register(DataModule)
class DataModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'status')


@admin.register(HNApiProduct)
class HNApiProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'status')


@admin.register(JsonConfig)
class JsonConfigAdmin(admin.ModelAdmin):
    list_display = ('name',)


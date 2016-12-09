# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import export_customers, export_projects, export_data_businessman, export_data_customer


urlpatterns = patterns('',
    url(r'^customers/$', export_customers, name='export-customers'),
    url(r'^projects/$', export_projects, name='export-projects'),
    url(r'^data-businessman/$', export_data_businessman, name='export-data-businessman'),
    url(r'^data-customer/$', export_data_customer, name='export-data-customer'),
)

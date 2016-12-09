# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from category import ajax_category


urlpatterns = patterns('',

    url(r'^options/$', ajax_category),
)

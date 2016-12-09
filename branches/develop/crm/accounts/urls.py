# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import LoginView, ChangepwdView


urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'accounts.views.logout_view', name='logout'),
    url(r'^profile/$', 'accounts.views.profile_view', name='profile'),
    url(r'^changepwd/$', login_required(ChangepwdView.as_view()), name='changepwd'),
    url(r'^changepwddone/$', 'accounts.views.changepwd_done', name='changepwddone'),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.conf import settings
# from django.contrib.auth.decorators import login_required

from accounts.views import LoginView


urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^crm/', include('crm.urls')),
    url(r'^export/', include('export.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )

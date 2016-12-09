from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static

from accounts.views import LoginView


urlpatterns = patterns('',

    url(r'^$', LoginView.as_view(), name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^crm/', include('crm.urls')),
    url(r'^export/', include('export.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import include, url
from django.contrib.auth.models import User
# from rest_framework import routers, serializers,
from rest_framework.authtoken import views
from django.conf.urls import patterns, include, url
from views import ObtainExpiringAuthToken
from authentication import ExpiringTokenAuthentication
from api.customers import ApiCustomers
from api.projects import  ApiProgress,ApiProjects
from api.contacts import  ApiProjectsContact
from common import get_config
urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token/', ExpiringTokenAuthentication,  ## token auth
    url(r'^login$', ObtainExpiringAuthToken.as_view()),  ## token auth
    url(r'^customers$', ApiCustomers.as_view()),
    url(r'^projects$', ApiProjects.as_view()),
    url(r'^projects/progress$', ApiProgress.as_view()),
    url(r'^projects/contacts$', ApiProjectsContact.as_view()),
    url(r'^getConfig$',get_config),
    # url(r'^projects/contacts', ApiContacts.as_view()),
   
)

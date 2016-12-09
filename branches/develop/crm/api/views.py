# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import datetime
from django.utils.timezone import utc
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from durationfield.db.models.fields.duration import DurationField as ModelDurationField
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import routers
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from authentication import ExpiringTokenAuthentication
import logging
import traceback
####################
from accounts.models import UserCredit
ERR_LOG = logging.getLogger('crm_api_error')
#ObtainExpiringAuthToken, works for Django 1.7+
EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 30)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        e = ''
        status = 1
        try:
            serializer = self.serializer_class(data=request.data)
            messageid = request.data['messageid'].strip()
            username = request.data['username'].strip()
        except Exception, e:
            messageid = ''
            status = 0
            ERR_LOG.error(traceback.format_exc())

        #igt_task.delay()
        try:
            usercredit = UserCredit.objects.get(user__username = username)
            usertype = usercredit.role.id
        except Exception, e:
            usertype = ''
            status = 0
            ERR_LOG.error(traceback.format_exc())
        if serializer.is_valid():
            request_data = request.data
            clientid = request_data.get("clientid","")
            DeviceToken = request_data.get("DeviceToken","")
            if clientid  and clientid != usercredit.cid: 
                usercredit.cid = clientid
                usercredit.save()
            if DeviceToken and DeviceToken != usercredit.devicetoken:
                usercredit.devicetoken = DeviceToken
                usercredit.save()
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
            utc_now = datetime.datetime.utcnow().replace(tzinfo=None)
            if not created or token.created < utc_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                #update the created time of the token to keep it valid
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()
            return Response({'token': token.key,
                            "messageid" : messageid ,
                            "usertype":usertype,
                            "status":status, 
                            "fail_reason":e,
                            "zone_id": uercredit.zone.id,
                            "uid":usercredit.id
                            })
        return Response({'token':u"",
                            "messageid" : messageid ,
                            "usertype":usertype,
                            "status":0, 
                            "fail_reason":'用户名或密码错误',
                            })
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class SnippetList(APIView):
    """
    列出所有代码片段(snippets), 或者新建一个代码片段(snippet).
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        #serializer = self.serializer_class(User.objects.all())
        queryset = User.objects.all()
        #serializer = UserSerializer
        s= serializers(User.objects.all())
        print s
        return Response(request.data)

    def post(self, request, format=None):
        token = request.META['HTTP_AUTHORIZATION'][5:].strip()
        #print request.POST
        try:
            serializer = ExpiringTokenAuthentication().authenticate_credentials(key = token)
        except Exception, e:
            raise e
        else:
            pass
        #print serializer
        if serializer:
            print 'success'
            # serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
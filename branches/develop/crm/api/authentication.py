#!coding=utf-8
from __future__ import unicode_literals
import datetime
from django.utils.timezone import utc
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.response import Response
from models import Token
EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 30)

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key,):
        #print self.request.GET,self.request.POST
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return u"不合法的Token"
            #raise exceptions.AuthenticationFailed('Invalid token ')
        if not token.user.is_active:
            return u"用户不存在或者被管理员设置为不可登录用户"
            #aise exceptions.AuthenticationFailed('User inactive or deleted')
        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if token.created < utc_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
            return u'Token过期请重新登陆'
            #raise exceptions.AuthenticationFailed(u'Token 过期 请重新登陆')
        #正确返回１
        return 1
        #return (token.user, token)

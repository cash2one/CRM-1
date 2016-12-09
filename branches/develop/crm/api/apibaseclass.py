# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import logging
import traceback
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
###　自定义的包　start
from authentication  import ExpiringTokenAuthentication
### 自定义的包　end
ERR_LOG = logging.getLogger('crm_api_error')

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
class BaseApiAuth(APIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (ExpiringTokenAuthentication,)
    def check_auth_token(self, request ,key):
        try:
            serializer = ExpiringTokenAuthentication().authenticate_credentials(key = key)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
            return serializer
        finally:
            return serializer
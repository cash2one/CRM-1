# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import logging
import traceback
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status ,mixins ,generics ,permissions ,renderers
from rest_framework.reverse import reverse
from django.http import HttpResponse
###　自定义的包　start
from serializers import ContactSerializer
from crm.models  import Contact,Project
from accounts.models import UserCredit
from .models import Token
from apibaseclass import JSONResponse,BaseApiAuth
from .common import TIMEDT
### 自定义的包　end
ERR_LOG = logging.getLogger('crm_api_error')

class ApiProjectsContact(BaseApiAuth):
    def post(self, request, format=None):
        try:
            api_data = request.data
            key = api_data.get('token','').strip()
            messageid = api_data.get('messageid','').strip()
        except Exception, e:
            check_auth_token = e
            ERR_LOG.error(traceback.format_exc())
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            serializer = ContactSerializer(data=api_data)
            if serializer.is_valid():
                serializer.save()
                if api_data["projectid"]:
                    try:
                        project = Project.objects.get(id = api_data["projectid"])
                        contact = Contact.objects.get(id = int(serializer.data["id"]))
                    except Exception, e:
                        return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":e,
                            })
                    project.contacts.add(contact)
                    project.save()
                    return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":"",
                            })
                    #return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":serializer.errors,
                            })
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ##如果Token　是不合法的则返回错误原因
        else:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token,
                            })
    def delete(self,request ,format = None):
        error = ''
        try:
            messageid = request.GET.get('messageid','').strip()
            key = request.GET.get('token','').strip()
            contactid = request.GET.get("contact_id",'')
            projectid = request.GET.get("project_id","")
            token =Token.objects.filter(pk = key).first()
        except Exception, e:
            error = e
            ERR_LOG.error(traceback.format_exc())
  
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            try:
                contact = Contact.objects.get(id= int(contactid))
            except Contact.DoesNotExist as e:
                return JsonResponse({'msg': unicode(e)})
            if contact.testapply_set.exists():
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":u"有测试申请用到这个联系人！",
                            })
            if contact.impapply_set.exists():
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":u"有交付申请用到这个联系人！",
                            })
            contact.delete()
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":"",
                            })
        ##如果Token　是不合法的则返回错误原因
        else:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token + error,
                            })
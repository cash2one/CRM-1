# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import logging
import traceback
import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
#from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,mixins ,generics ,permissions ,renderers
from rest_framework.reverse import reverse
from rest_framework.permissions  import IsAuthenticated
from django.http import HttpResponse
from rest_framework.parsers import JSONParser

###　自定义的包　stat
from apibaseclass import JSONResponse,BaseApiAuth
from serializers import CustomersSerializer
from crm.models  import Customer
from .models import Token
from .common import TIMEDT
from accounts.models import UserCredit
### 自定义的包　end


ERR_LOG = logging.getLogger('crm_api_error')
class ApiCustomers(BaseApiAuth):
    ##获取查询参数
    def get_parameter(self,request):
        parameter = {}
        parameter["messageid"]  = request.GET.get("messageid","").strip()
        parameter["token"] = request.GET.get("token","").strip()
        parameter["customer_id"] = request.GET.get("customer_id","")
        parameter["customer_type_id"] = request.GET.get("customer_type_id","")
        parameter["customer_priority"] =request.GET.get("customer_priority","")
        parameter["search_nearly_days"] =request.GET.get("search_nearly_days","")
        parameter["customer_name"] =request.GET.get("customer_name","").strip()
        parameter["search_customer_createtime_start"] =request.GET.get("search_customer_createtime_start","").strip()
        parameter["search_customer_createtime_end"] =request.GET.get("search_customer_createtime_end","").strip()
        return parameter
    def query_customer(self,customers, date_start, date_end):
        """根据post请求数据查询Customer"""
        if date_start and date_end:
            now = timezone.now()
            date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
            date_start = now.replace(year=date_start.year, month=date_start.month, day=date_start.day,
                                     hour=0, minute=0, second=0, microsecond=0)
            date_end = now.replace(year=date_end.year, month=date_end.month, day=date_end.day,
                                   hour=0, minute=0, second=0, microsecond=0)
            date_end = date_end + datetime.timedelta(days=1)
            print date_start,date_end
            customers = customers.filter(timestamp__gte=date_start).filter(timestamp__lt=date_end).all()
        return customers

    def filter_customers(self,customers, parameter):
        """ 根据客户类型,客户级别,时间区间筛选客户 """
        if parameter["customer_id"]  :
            customers = customers.filter(id = int(parameter["customer_id"]))
        if parameter["customer_name"]:
            customers = customers.filter(name= parameter["customer_name"])
        if parameter["customer_type_id"] and parameter["customer_type_id"] <> "0":
            customers = customers.filter(type__id=int(parameter["customer_type_id"]))
        if parameter["customer_priority"] :
            customers = customers.filter(priority= int(parameter["customer_priority"] ))
        if parameter["search_nearly_days"]:
            now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            period = now - TIMEDT[int(parameter["search_nearly_days"])]
            customers = customers.filter(timestamp__gte=period)
        date_start = parameter["search_customer_createtime_start"]
        date_end = parameter["search_customer_createtime_end"]
        if date_start and date_end:
            customers =  self.query_customer(customers, date_start, date_end)
        if parameter["token"]:
            try:
                token =Token.objects.filter(pk = parameter["token"]).first()
                usercredit = UserCredit.objects.filter(user = token.user).first()
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
            ##
            if usercredit.role.role == u'商务':
                customers = customers.filter(businessman__user= token.user)
        customers = customers.filter(is_delete=False)
        return customers
    ##处理get请求
    def get(self, request, format=None):
        messageid = request.GET.get("messageid",'')
        key = request.GET.get('token','')
        check_auth_token = self.check_auth_token(request,key = key )
        try:
            token =Token.objects.filter(pk = key).first()
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        ##如果Token 是正确的进行筛选
        if key and check_auth_token == 1:
            customers = Customer.objects.all().filter(is_delete=False)
            parameter = self.get_parameter(request)
            customers = self.filter_customers(customers ,parameter)
            serializer = CustomersSerializer(customers, many=True)
            return_api_data = {}
            return_api_data['messageid'] = messageid
            return_api_data['records'] =  serializer.data
            return_api_data['status'] = 1
            return_api_data['fail_reason'] = ''
            return JSONResponse(return_api_data)
        ##如果Token　是不合法的则返回错误原因
        else:
            return Response({'token':request.GET.get("token",''),
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token,
                            })
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
            customer_name = request.data.get('name','')
            check_customer = Customer.objects.filter(name = customer_name)
            if check_customer:
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":"客户已经存在",
                            "id":""
                            })
            serializer = CustomersSerializer(data=api_data)
            if serializer.is_valid():
                serializer.save()
                #print serializer.data["id"]
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":"",
                            "id":serializer.data["id"]
                            })
                #return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":serializer.errors,
                            })
        ##如果Token　是不合法的则返回错误原因
        else:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token,
                            })
    def put(self,request ,format = None):
        try:
            api_data = request.data
            key = api_data.get('token','').strip()
            messageid = api_data.get('messageid','').strip()
            customer_id = api_data.get('customerid','')
            customer = Customer.objects.filter(id = int(customer_id),is_delete=False)
        except Exception, e:
            check_auth_token = e
            ERR_LOG.error(traceback.format_exc())
        if not customer:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":u"该客户不存在",
                            })
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            serializer = CustomersSerializer(customer.first(),data=api_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":"",
                            })
                #return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":serializer.errors,
                            })
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
            key = request.GET.get('token','').strip()
            messageid = request.GET.get('messageid','').strip()
            customer_id = request.GET.get('id','')
            customer = Customer.objects.filter(id = int(customer_id))
        except Exception, e:
            error = e
            ERR_LOG.error(traceback.format_exc())
        if not customer:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":u"该客户不存在",
                            })
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            #customer.delete()
            customer[0].is_delete = True
            customer[0].save()
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason": error,
                            })
        ##如果Token　是不合法的则返回错误原因
        else:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token + error,
                            })




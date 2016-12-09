# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import logging
import traceback
import datetime
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
from serializers import ProjectsSerializer,ProgressSerializer,ProjectsSerializerGet
from crm.models  import Project,Progress
from accounts.models import UserCredit
from .models import Token
from apibaseclass import JSONResponse,BaseApiAuth
from .common import TIMEDT
### 自定义的包　end
ERR_LOG = logging.getLogger('crm_api_error')

class ApiProjects(BaseApiAuth):
    ##获取查询参数
    def get_parameter(self,request):
        parameter = {}
        parameter["messageid"]  = request.GET.get("messageid","").strip()
        parameter["token"] = request.GET.get("token","").strip()
        parameter["customer_priority"] =request.GET.get("customer_priority","").strip()
        parameter["progress"] = request.GET.get("progress","").strip()
        parameter["product_id"] = request.GET.get("product_id","").strip()
        parameter["project_name"] = request.GET.get("project_name","").strip()
        parameter["projectid"] = request.GET.get("projectid","")
        parameter["search_nearly_days"] =request.GET.get("search_nearly_days","").strip()
        parameter["customer_name"] =request.GET.get("customer_name","").strip()
        parameter["search_project_createtime_start"] =request.GET.get("search_project_createtime_start","").strip()
        parameter["search_project_createtime_end"] =request.GET.get("search_project_createtime_end","").strip()
        return parameter

    def query_project(self,projects,date_start="", date_end=""):
        if date_start and date_end:
            now = timezone.now()
            date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
            date_start = now.replace(year=date_start.year, month=date_start.month, day=date_start.day,
                                     hour=0, minute=0, second=0, microsecond=0)
            date_end = now.replace(year=date_end.year, month=date_end.month, day=date_end.day,
                                   hour=0, minute=0, second=0, microsecond=0)
            date_end = date_end + datetime.timedelta(days=1)
            projects = projects.filter(progress__updatetime__gte=date_start).filter(progress__updatetime__lt=date_end).all().distinct()
        return projects
    def filter_projects(self,projects, parameter):
        """ 根据客户类型,客户级别,时间区间筛选客户 """
        if parameter["token"]:
            try:
                token =Token.objects.filter(pk = parameter["token"]).first()
                usercredit = UserCredit.objects.filter(user = token.user).first()
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
            ##
            if usercredit.role.role == u'商务':
                projects = projects.filter(Q(customer__businessman = usercredit) | Q(businessman = usercredit))

                # projects = usercredit.project_set.filter(is_delete=False)
                # print projects
        if parameter["customer_priority"]  :
            projects = projects.filter(customer__priority = parameter["customer_priority"])
        if parameter['progress'] :
            def filter_by_progress(project):
                #progress = Progress.PROGRESS_CHOICES[int(parameter['progress'])][1]
                if not project.progress_set.exists():

                    return project.progress_set.latest('updatetime').progress == int(parameter['progress'])
            #filter(filter_by_progress, projects)
            filter(filter_by_progress, projects)
        if parameter['product_id']:
            projects = projects.filter(products__id = int(parameter['product_id']))
        if parameter["project_name"]:
            projects = projects.filter(name = parameter["project_name"])
        if parameter["projectid"]:
            projects = projects.filter(id  = int(parameter["projectid"]))
        if parameter["customer_name"] :
            projects = projects.filter(Q(customer__name = parameter["customer_name"]) | Q(customer__short_name = parameter["customer_name"]))
        if parameter["search_nearly_days"]:
            now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            period = now - TIMEDT[int(parameter["search_nearly_days"])]
            projects = projects.filter(timestamp__gte=period)
        date_start = parameter["search_project_createtime_start"]
        date_end = parameter["search_project_createtime_end"]
        if date_start and date_end:
            projects =  self.query_project(projects, date_start, date_end)
        
        projects = projects.filter(is_delete=False)
        return projects.distinct()
    def add_latest_progress_to_project(self,projects):
        serializers = ProjectsSerializerGet(projects, many=True)
        projects = Project.objects.all()
        progress_project = Progress.objects.all()
        for serializer in serializers.data:
            progress_data = []
            try:
                project_id = serializer["id"]
                latest_progress = projects.filter(id = project_id).first().get_latest_progress()
                progress = progress_project.filter(project__id = project_id)
                if progress:
                    progress_data = ProgressSerializer(progress,many = True)
                    serializer["progress"] = progress_data.data 
                else:
                    serializer["progress"] = []
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
            else:
                if latest_progress:
                    serializer['latest_progress'] = latest_progress.progress
                    serializer['description'] = latest_progress.description
                    serializer['plan'] = latest_progress.plan
                    serializer['operator'] = latest_progress.operator 
                else: 
                    serializer['latest_progress'] = ""
                    serializer['description'] = ""
                    serializer['plan'] = ""
                    serializer['operator'] =  "" 
            
        return   serializers 
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
            projects = Project.objects.all()
            parameter = self.get_parameter(request)
            projects = self.filter_projects(projects, parameter)
            serializer = self.add_latest_progress_to_project(projects)
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
            serializer = ProjectsSerializer(data=api_data)
            #serializer = ProjectsSerializerCreate(data=api_data)
            if serializer.is_valid():
                serializer.save()
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
            projectid = api_data.get('projectid','')
            project = Project.objects.filter(id = int(projectid),is_delete=False)
        except Exception, e:
            check_auth_token = e
            ERR_LOG.error(traceback.format_exc())
        if not project:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":"项目不存在",
                            })
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            serializer = ProjectsSerializer(project.first(),data=api_data)
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
        key = request.GET.get('token','').strip()
        if key:
            try:
                token =Token.objects.filter(pk = key).first()
                usercredit = UserCredit.objects.filter(user = token.user).first()
            except Exception, e:
                ERR_LOG.error(traceback.format_exc())
            projects = Project.objects.filter(businessman = usercredit)
        try:
            
            messageid = request.GET.get('messageid','').strip()
            
            project_id = request.GET.get('id','')
            print project_id
            project = projects.filter(id = int(project_id))
        except Exception, e:
            error = e
            ERR_LOG.error(traceback.format_exc())
        if not project:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":u"该项目不存在",
                            })
        check_auth_token = self.check_auth_token(request,key = key )
        if key and check_auth_token == 1:
            #project.delete()
            project[0].is_delete = True
            project[0].save()
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

###########################
# 给项目添加进度
###########################
class ApiProgress(BaseApiAuth):
    #处理get请求
    def get(self, request, format=None):
        messageid = request.GET.get("messageid",'')
        projectid = request.GET.get("projectid",'')
        key = request.GET.get('token','')
        check_auth_token = self.check_auth_token(request,key = key )
        try:
            token =Token.objects.filter(pk = key).first()
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        ##如果Token 是正确的进行筛选
        if key and check_auth_token == 1:
            if projectid :
                progress = Progress.objects.all().filter(project__id = int(projectid))
            
            serializer = ProgressSerializer(progress,many = True)
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
            serializer = ProgressSerializer(data=api_data)
            if serializer.is_valid():
                serializer.save()
                #return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason":"",
                            })
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
    # def put(self,request ,format = None):
    #     try:
    #         api_data = request.data
    #         key = api_data.get('token','').strip()
    #         messageid = api_data.get('messageid','').strip()
    #         customer_id = api_data.get('customerid','')
    #         customer = Customer.objects.get(id = int(customer_id),is_delete=False)
    #     except Exception, e:
    #         check_auth_token = e
    #         ERR_LOG.error(traceback.format_exc())
    #     check_auth_token = self.check_auth_token(request,key = key )
    #     if key and check_auth_token == 1:
    #         serializer = ProjectsSerializer(customer,data=api_data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     ##如果Token　是不合法的则返回错误原因
    #     else:
    #         return Response({'token': key,
    #                         "messageid" :messageid,
    #                         "status":0, 
    #                         "fail_reason":check_auth_token,
    #                         })
    # def delete(self,request ,format = None):
    #     error = ''
    #     try:
    #         key = request.GET.get('token','').strip()
    #         messageid = request.GET.get('messageid','').strip()
    #         customer_id = request.GET.get('id','')
    #         customer = Customer.objects.filter(id = int(customer_id))
    #     except Exception, e:
    #         error = e
    #         ERR_LOG.error(traceback.format_exc())
    #     if not customer:
    #         return Response({'token': key,
    #                         "messageid" :messageid,
    #                         "status":0, 
    #                         "fail_reason":u"该客户不存在",
    #                         })
    #     check_auth_token = self.check_auth_token(request,key = key )
    #     if key and check_auth_token == 1:
    #         customer.delete()
    #         return Response({'token': key,
    #                         "messageid" :messageid,
    #                         "status":1, 
    #                         "fail_reason":str(check_auth_token) + error,
    #                         })
    #     ##如果Token　是不合法的则返回错误原因
    #     else:
    #         return Response({'token': key,
    #                         "messageid" :messageid,
    #                         "status":0, 
    #                         "fail_reason":check_auth_token + error,
    #                         })

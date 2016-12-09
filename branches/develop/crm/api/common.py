# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import logging
import traceback
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from accounts.models import Role,UserCredit
from serializers import UserCreditSerializer
from apibaseclass import BaseApiAuth
from .models import Token
from crm.models import (Customer, CustomerType, 
					CustomerCategory1, CustomerCategory2, 
					CustomerCategory3,Progress,Product)
from accounts.models import Zone
ERR_LOG = logging.getLogger('crm_api_error')
TIMEDT = {
    1: datetime.timedelta(days=3),
    2: datetime.timedelta(days=7),
    3: datetime.timedelta(days=15)
}
USER_TYPE = {
    
}
def ajax_category():
    """获取客户三级类目各级的选项"""
    category1 = CustomerCategory1.objects.all()
    category2 = CustomerCategory2.objects.all()
    category3 = CustomerCategory3.objects.all()
    data = {
        'c1': [{'id': c.id, 'name': c.name} for c in category1],
        'c2': {},
        'c3': {},
    }
    category1_id_list = list(set([c.category1.id for c in category2]))
    for c1_id in category1_id_list:
        if CustomerCategory2.objects.filter(category1=c1_id).exists():
            data['c2'][c1_id] = [{'id': c2.id, 'name': c2.name} for c2 in CustomerCategory2.objects.filter(category1=c1_id).all()]

    category2_id_list = list(set([c.category2.id for c in category3]))
    for c2_id in category2_id_list:
        if CustomerCategory3.objects.filter(category2=c2_id).exists():
            data['c3'][c2_id] = [{'id': c3.id, 'name': c3.name} for c3 in CustomerCategory3.objects.filter(category2=c2_id).all()]
    return data

@api_view(['POST',"GET"])
@csrf_exempt
def get_config(request):
	try:
	        api_data = request.data
	        key = api_data.get('token','').strip()
	        messageid = api_data.get('messageid','').strip()
	except Exception, e:
	    check_auth_token = e
	    ERR_LOG.error(traceback.format_exc())
	try:
	    token =Token.objects.filter(pk = key).first()
	    usercredit = UserCredit.objects.filter(user = token.user).first()
	except Exception, e:
	    ERR_LOG.error(traceback.format_exc())
	check_auth_token = BaseApiAuth().check_auth_token(request,key = key )
	if key and check_auth_token == 1:
		config = {}
		progress = Progress.PROGRESS_CHOICES
		customerPriority = Customer.PRIORITY_CHOICES
		zone = Zone.objects.all().values_list("id","name")
		role = Role.objects.all().values_list()
		product_list = Product.objects.all()
		product_dict = {}
		for i  in product_list:
			product_dict[i.id] = i.name
		zoneType = dict(zone)
		userType = dict(role)
		progress = dict(progress)
		config["userType"] = userType
		config["ZoneType"] = zoneType
		config["progress"] = progress
		config["customerPriority"] = dict(customerPriority)
		config["product"] = product_dict
		try:
			usercredit = UserCredit.objects.filter(zone = usercredit.zone,role=usercredit.role)
		except Exception, e:
			ERR_LOG.error(traceback.format_exc())
		member_group = []
		serializer = UserCreditSerializer(usercredit , many = True)
		for userc  in serializer.data:
			member_group.append({"usercredit_id":userc["id"],"name":userc["user"]["first_name"]})
		config["memberGroup"] = member_group
		cat1_list= CustomerCategory1.objects.all()
		cat = {}

		try:
			customerstype = CustomerType.objects.all().values_list("id","name")
			customerstype = dict(customerstype)
		except Exception, e:
			ERR_LOG.error(traceback.format_exc())
		config["customerType"] = customerstype
		config["data"] = ajax_category()
  		return  Response({'token': key,
                            "messageid" :messageid,
                            "status":1, 
                            "fail_reason": "",
                            "configData":config
                            })
	else:
            return Response({'token': key,
                            "messageid" :messageid,
                            "status":0, 
                            "fail_reason":check_auth_token ,
                            })


    #return JsonResponse({'msg': 0, 'data': data})
if __name__ == '__main__':
	usercredit = UserCredit.objects.get(user__first_name = "root")
	get_config(usercredit)
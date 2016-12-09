# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from django.contrib.auth.models import User
from crm.models import (Customer,CustomerType,CustomerCategory1,CustomerCategory2,CustomerCategory3,
                        Project,Contact,Progress,Product)
from accounts.models import UserCredit,Role,Zone
from i_bankserver.models import BProduct
from .models import Token
import logging
import traceback
ERR_LOG = logging.getLogger('crm_api_error')
# class SnippetSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         传入验证过的数据, 创建并返回`Snippet`实例。
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         传入验证过的数据, 更新并返回已有的`Snippet`实例。
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class CustomerCategory1Serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCategory1
        exclude = ("id",)
class CustomerCategory2Serializer(serializers.ModelSerializer):
    category1 = CustomerCategory1Serializer(read_only = True)
    class Meta:
        model = CustomerCategory2
        exclude = ("id",)
class CustomerCategory3Serializer(serializers.ModelSerializer):
    category2 = CustomerCategory2Serializer(read_only = True)
    class Meta:
        model = CustomerCategory3
        exclude = ("id",)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        exclude = ("id","password")
class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        exclude = ("id",)
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        exclude = ("id",)
class UserCreditSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # role = RoleSerializer()
    # #role = serializers.StringRelatedField()
    # zone = ZoneSerializer()
    class Meta:
        model = UserCredit
        extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        #exclude = ("id",)
        fields = '__all__'
class CustomerTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False,read_only=True)
    class Meta:
        model = CustomerType
        fields = '__all__'
        #extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        # exclude = ("id",)
class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False,read_only=True)
    class Meta:
        model = Contact
        #fields = '__all__'
        #extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        exclude = ('is_delete',)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        #extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        #exclude = ("id",'is_delete')
class CustomersSerializer(serializers.ModelSerializer):
    #owner = serializers.Field(source='owner.username')
    #tracks = TrackSerializer(many=True, read_only=True)
    #groups = serializers.PrimaryKeyRelatedField(many=True ,read_only=True)
    ####处理外键的代码　start
    #businessman= serializers.StringRelatedField(many=True ,read_only=True)
    businessman = UserCreditSerializer(many=True, read_only=True)
    #category1 = serializers.StringRelatedField(read_only=True)
    #category2 = serializers.StringRelatedField(read_only=True)
    #category3 = serializers.StringRelatedField(read_only=True)
    # #type = CustomerTypeSerializer(read_only = True)
    # zone = ZoneSerializer(read_only=True)
    # type = CustomerTypeSerializer(read_only = True)
    ####处理我外键的代码end
    class Meta:
        model = Customer  
        #exclude = ("is_delete",)　　
        #fields = '__all__'  #显示所有的字段
        #fields = ('name', 'short_name', 'type', 'category1', 'category2', 'category3', 
        	      # 'priority','zone',"province","city","address",
        	      # "businessman","registered_capital","shareholder",
        	      # "product_desc","notes","timestamp","is_delete",)
        #extra_kwargs = {'id': {'read_only': False, 'required': False}} 
        exclude = ("is_delete",)
    def create(self, validated_data):
        """
        传入验证过的数据, 创建并返回`customer`实例。
        """
        customer = super(CustomersSerializer, self).create(validated_data)
        #customer = Customer.objects.create(**validated_data)
        all_parameter = self.initial_data
        try:
            key = all_parameter['token']
            token =Token.objects.filter(pk = key).first()
            usercredit = UserCredit.objects.get(user = token.user)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        # print customer.zone,"tyr"
        # try:
        #     zone = usercredit.zone
        #     customer.zone =  zone 
        #     print customer.zone,"tyr"
        # except Exception, e:
        #     ERR_LOG.error(traceback.format_exc())
        try:
            businessmans_id = all_parameter['businessman'] + [usercredit.id]
            businessmans = UserCredit.objects.filter(id__in=businessmans_id).all()
            customer.businessman.add(*businessmans)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        return customer

    def update(self, instance, validated_data):
        instance = super(CustomersSerializer, self).update(instance, validated_data)
        all_parameter = self.initial_data
        try:
            key = all_parameter['token']
            token =Token.objects.filter(pk = key).first()
            usercredit = UserCredit.objects.get(user = token.user)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        try:
            businessmans_id = all_parameter['businessman'] + [usercredit.id]
            businessmans = UserCredit.objects.filter(id__in=businessmans_id).all()
            instance.businessman = businessmans
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        instance.save()
        return instance
class ProjectsSerializer(serializers.ModelSerializer):
    #businessman= serializers.StringRelatedField(many=True ,read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True ,read_only=True)
    #customer = CustomersSerializer(read_only=True)
    #progress = ProgressSerializer(many=True, read_only=True)
    class Meta:
        model = Project  
        exclude = ("is_delete",)
    def create(self, validated_data):
        """
        传入验证过的数据, 创建并返回`project`实例。

        """
        project = super(ProjectsSerializer, self).create(validated_data)
        all_parameter = self.initial_data
        #project = Project.objects.create(**validated_data)
        try:
            key = all_parameter['token']
            token =Token.objects.filter(pk = key).first()
            usercredit = UserCredit.objects.get(user = token.user)
            project.businessman.add(usercredit)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        try:
            product_list = all_parameter['products']
            products_list = Product.objects.filter(id__in = product_list).all()
            project.products.add(*products_list)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        contacts = []
        try:
            for contact in all_parameter['contacts']:
                contact = Contact.objects.create(
                    name=contact["name"],
                    position=contact["position"],
                    tel=contact["tel"],
                    mobile=contact["mobile"],
                    email=contact["email"],
                )
                contacts.append(contact)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        project.contacts.add(*contacts)
        return project
    def update(self, instance, validated_data):
        """
        传入验证过的数据, 更新并返回已有的`project`实例。
        """
        instance = super(ProjectsSerializer, self).update(instance, validated_data)
        all_parameter = self.initial_data
        try:
            product_list = all_parameter['products']
            products_list = Product.objects.filter(id__in = product_list).all()
            instance.products.clear()
            instance.products.add(*products_list)
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        try:
            customer = Customer.objects.get( id = all_parameter['customer'])
            instance.customer = customer
        except Exception, e:
            ERR_LOG.error(traceback.format_exc())
        instance.name = all_parameter['name']
        instance.notes = all_parameter['notes']
        instance.save()
        return instance
class ProjectsSerializerCreate(ProjectsSerializer):
    """docstring for ClassName"""
    
    def __init__(self):
        super(ProjectsSerializerCreate, self).__init__()
    businessman= serializers.StringRelatedField(many=True ,read_only=True) 


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields =  '__all__'
class CustomersSerializerForProject(serializers.ModelSerializer):
    class Meta:
        model = Customer  
        exclude = ("is_delete",) 
class ProjectsSerializerGet(ProjectsSerializer):
    customer = CustomersSerializerForProject(read_only=True)
class BproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BProduct
        # fields =  (
        #         "id",
        #         "code",
        #         "name",
        #         "type"
        #     )
        fields =  '__all__'
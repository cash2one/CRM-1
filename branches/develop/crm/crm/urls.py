# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from .customers import (
    CustomersMine, CustomersAll, CustomerList, CustomerAdd, ajax_customer_add,
    customer_edit, ajax_customer_edit, customer_view, ajax_customer_view, ajax_customer_del
)
from .projects import (
    Projects, ProjectList, ProjectListProduct,project_add, ajax_project_add, project_edit,
    ajax_project_edit, ajax_project_del, project_view
)
from .apply_views import *
from .views import *


urlpatterns = patterns('',

    url(r'^category/', include('crm.category_urls')),

    url(r'^customer/add/$', CustomerAdd.as_view(), name='customer-add'),
    url(r'^customer/edit/(\d+)/$', customer_edit, name='customer-edit'),
    url(r'^customer/view/(\d+)/$', customer_view, name='customer-view'),
    url(r'^ajax/customer/add/$', ajax_customer_add, name='ajax-customer-add'),
    url(r'^ajax/customer/edit/$', ajax_customer_edit, name='ajax-customer-edit'),
    url(r'^ajax/customer/view/$', ajax_customer_view, name='ajax-customer-view'),
    url(r'^ajax/customer/del/$', ajax_customer_del, name='ajax-customer-del'),
    url(r'^customers/mine/(?P<typeid>\d+)/(?P<priority>\d+)/(?P<time>\d+)/$', CustomersMine.as_view(), name='customers-mine'),
    url(r'^customers/all/(?P<typeid>\d+)/(?P<priority>\d+)/(?P<zoneid>\d+)/(?P<time>\d+)/$', CustomersAll.as_view(), name='customers-all'),
    url(r'^customer/list/(?P<typeid>\d+)/(?P<priority>\d+)/(?P<zoneid>\d+)/(?P<time>\d+)/$', CustomerList.as_view(), name='customer-list'),


    url(r'^project/add/$', project_add, name='project-add'),
    url(r'^project/edit/(\d+)/$', project_edit, name='project-edit'),
    url(r'^project/view/(\d+)/$', project_view, name='project-view'),
    url(r'^ajax/project/add/$', ajax_project_add, name='ajax-project-add'),
    url(r'^ajax/project/edit/$', ajax_project_edit, name='ajax-project-edit'),
    url(r'^ajax/project/del/$', ajax_project_del, name='ajax-project-del'),
    url(r'^projects/(?P<priority>\d+)/(?P<progress>\d+)/(?P<productid>\d+)/(?P<updatetime>\d+)/$', Projects.as_view(), name='projects'),
    url(r'^project/list/(?P<priority>\d+)/(?P<progress>\d+)/(?P<productid>\d+)/(?P<zoneid>\d+)/(?P<updatetime>\d+)/$', ProjectList.as_view(), name='project-list'),
    url(r'^project/list/product/(?P<priority>\d+)/(?P<progress>\d+)/(?P<productid>\d+)/(?P<zoneid>\d+)/(?P<updatetime>\d+)/$', ProjectListProduct.as_view(), name='project-list-product'),
    # url(r'^project/list/imp/(?P<impstate>\w+)/(?P<priority>\d+)/(?P<productid>\d+)/(?P<zoneid>\d+)/$', ProjectListImp.as_view(), name='project-list-imp'),


    # 测试申请
    url(r'^test-apply/add/view/(\d+)/$', TestApplyAddView.as_view(), name='test-apply-add-view'),
    url(r'^test-apply/add/$', ajax_test_apply_add, name='ajax-test-apply-add'),
    url(r'^test-apply/edit/view/(\d+)/$', TestApplyEditView.as_view()),
    url(r'^test-apply/edit/$', ajax_test_apply_edit),
    url(r'^test-apply/view/(\d+)/$', test_apply_view, name='test-apply-view'),
    url(r'^test-apply/del/$', test_apply_del),
    url(r'^test-apply/list/(?P<progress>\d+)/(?P<priority>\d+)/(?P<product_id>\d+)/$', TestApplyListView.as_view(), name='test-apply-list'),
    url(r'^test-apply/progress/add/(\d+)/$', test_apply_progress_add),

    # 交付申请
    url(r'^ajax/get-project-products/$', get_project_products, name='ajax-get-project-products'),
    url(r'^imp-apply/add/(\d+)/(\d+)/$', ImpApplyAdd.as_view(), name='imp-apply-add'),
    url(r'^imp-apply/edit/(\d+)/$', ImpApplyEdit.as_view(), name='imp-apply-edit'),
    url(r'^imp-apply/view/(\d+)/$', imp_apply_view, name='imp-apply-view'),
    url(r'^imp-apply/del/$', imp_apply_del),
    url(r'^imp-apply/list/(?P<progress>\d+)/(?P<priority>\d+)/(?P<product_id>\d+)/$', ImpApplyListView.as_view(), name='imp-apply-list'),
    url(r'^imp-apply/progress/add/(\d+)/$', imp_apply_progress_add),
    url(r'^imp-apply/free-date-start/edit/(\d+)/$', imp_apply_free_date_start_edit),
    #added new 
    url(r'^imp-apply/director/list/(?P<progress>\d+)/(?P<priority>\d+)/(?P<product_id>\d+)/$', ImpApplyDirectorListView.as_view(), name='imp-apply-director-list'),
    
    url(r'imp-apply/done/$', imp_apply_done),
    url(r'imp/page/config/', imp_modules_config),

    # 标注
    url(r'^ajax/mark/edit/$', ajax_mark_edit, name='ajax-mark-edit'),

    # 联系人
    url(r'^ajax/contact/add/$', ajax_contact_add, name='ajax-contact-add'),
    url(r'^ajax/contact/edit/$', ajax_contact_edit, name='ajax-contact-edit'),
    url(r'^ajax/contact/view/$', ajax_contact_view, name='ajax-contact-view'),
    url(r'^ajax/contact/del/$', ajax_contact_del, name='ajax-contact-del'),

    # 进度
    url(r'^ajax/progress/add/$', ajax_progress_add, name='ajax-progress-add'),
    url(r'^ajax/progress/edit/$', ajax_progress_edit, name='ajax-progress-edit'),
    url(r'^ajax/progress/del/$', ajax_progress_del, name='ajax-progress-del'),

    # 数据统计
    url(r'^data-businessman/$', DataBm.as_view(), name='data-businessman'),
    url(r'^data-customer/$', DataCustomer.as_view(), name='data-customer'),
)

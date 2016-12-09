# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import urllib
import urlparse

from django.views.generic import TemplateView
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.http import urlencode

from .mixins import LoginRequiredMixin


PROVINCES = ('北京市', '上海市', '天津市', '重庆市', '河北省', '河南省', '辽宁省', '黑龙江省',
             '吉林省', '江苏省', '浙江省', '山东省', '安徽省', '湖南省', '江西省', '湖北省',
             '甘肃省', '山西省', '陕西省', '福建省', '贵州省', '广东省', '青海省', '广西省',
             '海南省', '云南省', '四川省', '内蒙古', '新疆', '宁夏', '香港', '澳门', '台湾')

PRIORITY = ('高', '中', '低')

TIME_CHOICES = ((0, '不限'), (1, '近三天'), (2, '近七天'), (3, '近半个月'))

TIMEDT = {
    1: datetime.timedelta(days=3),
    2: datetime.timedelta(days=7),
    3: datetime.timedelta(days=15)
}

PAGENUM = 20  # 分页器每页条数


def list_group(l, c):
    """将列表按给定个数分组"""
    return [l[i:i+c] for i in xrange(0, len(l), c)]


def qs(url):
    """获取url中的查询参数"""
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


def add_qs(url, **kwargs):
    """添加url参数
    :param params 用这个关键字参数输入字典类型
    """
    kwargs.update(kwargs.pop('params', ''))
    query_string = urllib.urlencode(kwargs)
    if not query_string:
        return url
    if not qs(url):
        return url+'?'+query_string
    else:
        return url+'&'+query_string


def query_transform(**kwargs):
    """生成查询字符串
    urllib.urlencode() 这个中文会报错
    """
    return urlencode(kwargs)


def paginate(data, current_page=1, page_num=PAGENUM):
    paginator = Paginator(data, page_num)
    try:
        show_lines = paginator.page(current_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_lines = paginator.page(paginator.num_pages)
    return show_lines


class CommonView(LoginRequiredMixin, TemplateView):
    template_name = ''
    allowed_role = []

    def check_role(self):
        if self.allowed_role and self.request.user.usercredit.role.role not in self.allowed_role:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CommonView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.check_role()
        return super(CommonView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_role()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    def get_device_anti_fraud(self,request, *args, **kwargs):
        deviceSenvenElement = {}
        deviceSenvenElement["device_anti_fraud_platform_web"] = request.POST.get("device-anti-fraud-platform-web","")
        deviceSenvenElement["device_anti_fraud_platform_android"] = request.POST.get("device-anti-fraud-platform-android","")
        deviceSenvenElement["device_anti_fraud_platform_ios"] = request.POST.get("device-anti-fraud-platform-ios","")
        deviceSenvenElement["device_anti_fraud_platform_web_domin"] = request.POST.get("device-anti-fraud-platform-web-domin","")
        deviceSenvenElement["device_anti_fraud_platform_app_name"] = request.POST.get("device-anti-fraud-platform-app-name","")
        deviceSenvenElement["device_anti_fraud_event_borrow_money"] = request.POST.get("device-anti-fraud-event-borrow-money","")
        deviceSenvenElement["device_anti_fraud_event_registration"] = request.POST.get("device-anti-fraud-event-registration","")
        deviceSenvenElement["device_anti_fraud_event_login"] = request.POST.get("device-anti-fraud-event-login","")
        deviceSenvenElement["device_anti_fraud_test_env"] = request.POST.get("device-anti-fraud-test-env","")
        deviceSenvenElement["device_anti_fraud_ios_idfa"] = request.POST.get("device-anti-fraud-ios-idfa","")
        deviceSenvenElement["device_anti_fraud_ios_lng"] = request.POST.get("device-anti-fraud-ios-lng","")
        return deviceSenvenElement
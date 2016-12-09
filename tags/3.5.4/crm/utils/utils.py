# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2
import urllib
import json
import ssl
import re
import pytz

from django.http import HttpResponseRedirect
from django.utils.http import urlencode


# 处理2.7.9之后的ssl问题, 这里全局取消https的ssl验证
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

LOCAL_TZ = pytz.timezone('Asia/Shanghai')

EMAIL_PATTERN = re.compile("^([\.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+")


def email_validate(email):
    if EMAIL_PATTERN.match(email):
        return True
    else:
        return False


def back_to_referrer(f):
    """ 根据Referer返回上一页 """
    def new_f(*args, **kwargs):
        f(*args, **kwargs)
        request = args[0]
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return new_f


def utc_to_local(utc_dt):
    """ UTC转成本地时间 """
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return LOCAL_TZ.normalize(local_dt)


def format_time(time):
    try:
        return time.strftime('%F %H:%M')
    except AttributeError:
        return ''


def post_dts(url, **kwargs):
    """ login_name='dts账号'; user_name='客户名称'; city='客户城市', email=''; analy='analyser' """
    params = urlencode(kwargs)
    print params
    ret = urllib2.urlopen(url, params).read()
    print ret
    msg = json.loads(ret).get('msg')  # msg: success/mailerror/accounterror
    print msg
    if msg == 'success':
        return  'test'
    elif msg == 'emailError':
        raise ValueError(u'无法创建DTS账号，联系人的email地址在DTS系统中已经存在')
    else:
        raise ValueError(msg)


if __name__ == '__main__':
    # url = "https://dts.100credit.com/als/custom/create_user/"
    url = "http://192.168.162.108:8004/als/custom/create_user/"
    #print post_dts(url, login_name='test111', user_name='客户名称', city='北京',email='yu.guo@100credit.com', analy='风控经理1')
    print post_dts(url, login_name='guoyu_test31', user_name='客户名称', city='北京',email='yu.zhao@100credit.com', analy='分析师小明')

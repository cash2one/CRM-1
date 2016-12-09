#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import json
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def post_dts(url, **kwargs):
    # login_name='dts账号', user_name='客户名称', email='', analy='analyser'
    params = urllib.urlencode(kwargs)
    ret = urllib.urlopen(url, params).read()
    # msg: success/mailerror/accounterror
    msg = json.loads(ret).get('msg')
    print msg
    if msg != 'success':
        raise ValueError, msg
    return


if __name__ == '__main__':
    url = "https://dts.100credit.com/als/custom/create_user/"
    print post_dts(url, login_name='test111', user_name='客户名称', email='xue.bai@100credit.com', analy='分析师1')


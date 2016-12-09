#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

data = {'login_name':'test111', 'user_name':'客户名称', 'email':'xue.bai@100credit.com', 'analy':'分析师1'}

url = "https://dts.100credit.com/als/custom/create_user/"

# response = requests.post(url, data=json.dumps(data))
response = requests.post(url, data=data, verify=False)

print response.status_code
print json.loads(response.text)

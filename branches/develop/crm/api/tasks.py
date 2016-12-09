# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import task
import time
import logging
from api.igt import ApnMessage
INFO = logging.getLogger('crm_getui_info') 
# qidong celeery
# python manage.py celery worker --loglevel=info
@task()
def igt_test():
	for i in range(4):
		print i
		time.sleep(i)
@task()
def igt_task(title,body,cid,imp_apply):
	apn_msg = ApnMessage(
	        title=title,
	        body= body,
	        content='',)
	s = apn_msg.push_to_single(cid)
	INFO.info(s)
	INFO.info(imp_apply.id)
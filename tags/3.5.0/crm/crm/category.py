# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import CustomerCategory1, CustomerCategory2, CustomerCategory3


@login_required
def ajax_category(request):
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
    return JsonResponse({'msg': 0, 'data': data})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from jsonfield.forms import JSONFormField

from accounts.models import UserCredit
from common import PROVINCES
from accounts.models import Zone
from .models import Customer, Project, Product, Contact


def gen_field(field_property):
    """根据json定义生成form字段"""
    fields = {
        'text': forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=field_property['initial']),
        'textarea': forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), initial=field_property['initial']),
        'bool': forms.BooleanField(),
        'interger': forms.IntegerField(),
        'choice': forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'})),
        'multichoice': forms.MultipleChoiceField(widget=forms.SelectMultiple()),
        'checkbox': forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    }
    field = fields[field_property['type']]
    if 'label' in field_property:
        field.label = field_property['label']
    if 'required' in field_property:
        field.required = field_property['required']
        if field.required:
            field.help_text = u'(必填)'
    if 'initial' in field_property:
        field.initial = field_property['initial']
    if 'choices' in field_property:
        field.choices = list(enumerate(field_property['choices']))
    return field


class ImpApplyForm(forms.Form):

    ACCOUNT_TYPE = ((1, u'试用'), (2, u'正式'))

    nda = forms.BooleanField(label=u'是否已签署保密协', required=False)
    contract = forms.BooleanField(label=u'是否已签署正式合同', required=False)
    br_code = forms.BooleanField(label=u'是否部署百融代码', required=False)
    account_type = forms.ChoiceField(
            label=u'账号类型', choices=ACCOUNT_TYPE,
            widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(ImpApplyForm, self).__init__(*args, **kwargs)
        if extra and isinstance(extra, dict):
            for field, field_property in extra.items():
                self.fields[field] = gen_field(field_property)
                self.data[field] = field_property['initial']


class ImpApplyBaseForm(forms.Form):

    ACCOUNT_TYPE = ((1, u'试用'), (2, u'正式'))

    nda = forms.BooleanField(label=u'是否已签署保密协', required=False, widget=forms.RadioSelect)
    contract = forms.BooleanField(label=u'是否已签署正式合同', required=False, widget=forms.RadioSelect)
    br_code = forms.BooleanField(label=u'是否部署百融代码', required=False, widget=forms.RadioSelect)
    account_type = forms.ChoiceField(
            label=u'账号类型', choices=ACCOUNT_TYPE,
            widget=forms.Select(attrs={'class': 'form-control'})
    )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['timestamp']
        labels = {
            'name': u'客户全称：',
            'short_name': u'客户简称：',
            'type': u'客户类型：',
            'category1': u'客户一级类目：',
            'category2': u'客户二级类目：',
            'category3': u'客户三级类目：',
            'priority': u'客户级别：',
            'zone': u'区域：',
            'province': u'省份：',
            'city': u'城市',
            'address': u'详细地址：',
            'businessman': u'跟进商务：',
            'registered_capital': u'注册资本（万）：',
            'shareholder': u'股东：',
            'product_desc': u'客户业务或产品描述：',
            'notes': u'备注',
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.initial = self.initial or {
                'name': '',
                'short_name': '',
                'type': 0,
                'category1': 0,
                'category2': 0,
                'category3': 0,
                'priority': 3,
                'zone': 0,
                'province': 0,
                'city': '',
                'address': '',
                'businessman': [],
                'registered_capital': '',
                'shareholder': '',
                'product_desc': '',
                'notes': '',
        }
        self.fields['zone'].queryset = Zone.zone_use()
        self.fields['province'].choices = PROVINCES
        self.fields["type"].choices = list(self.fields["type"].choices)[1:]  # 去掉empty_label
        self.fields["zone"].choices = list(self.fields["zone"].choices)[1:]

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if Customer.objects.filter(name=name, is_delete=False).exists():
            raise forms.ValidationError(u'该客户名称已经存在')


class ImpForm(forms.Form):
    analyser = forms.ModelChoiceField(queryset=UserCredit.objects.filter(role__role=u'风控经理'))
    operations = forms.ModelChoiceField(queryset=UserCredit.objects.filter(role__role=u'运营经理'))
    imp_engineer = forms.ModelChoiceField(queryset=UserCredit.objects.filter(role__role=u'交付经理'))
    project = forms.ModelChoiceField(queryset=Project.objects.filter(is_delete=False))
    extra_fields = JSONFormField()
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())
    notes = forms.CharField(widget=forms.Textarea)


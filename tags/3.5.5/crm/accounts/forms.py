# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=24)


class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField(max_length=24)
    new_pwd = forms.CharField(max_length=24)
    new_pwd_again = forms.CharField(max_length=24)

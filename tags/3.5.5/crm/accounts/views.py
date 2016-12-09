# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['username'] = self.request.POST.get('username', '')
        context['password'] = self.request.POST.get('password', '')
        return context

    def post(self, request):
        context = self.get_context_data()
        if not all((context['username'], context['password'])):
            messages.info(request, u'用户名和密码不能为空！')
            return render(request, self.template_name, context)
        # 认证
        user = authenticate(username=context['username'], password=context['password'])
        if user is not None and user.is_active:
            login(request, user)
            return redirect(redirect_url(user.usercredit.role.role))
        else:
            messages.info(request, u'用户名或密码错误！')
            return render(request, self.template_name, context)

def redirect_url(role):
    """根据登录用户的角色定向到不同的地址"""
    role_page = {
        u'管理层': reverse('customer-list', kwargs={'typeid': 0, 'priority': 0, 'zoneid': 0, 'time': 0}),
        u'商务总监': reverse('customer-list', kwargs={'typeid': 0, 'priority': 0, 'zoneid': 0, 'time': 0}),
        u'商务': reverse('customers-mine', kwargs={'typeid': 0, 'priority': 0, 'time': 0}),
        u'运营经理': reverse('customer-list', kwargs={'typeid': 0, 'priority': 0, 'zoneid': 0, 'time': 0}),
        u'风控经理': reverse('test-apply-list', kwargs={'progress': 1, 'priority': 0, 'product_id': 0}),
        u'交付经理': reverse('imp-apply-list', kwargs={'progress': 1, 'priority': 0, 'product_id': 0}),
        u'交付总监': reverse('imp-apply-list', kwargs={'progress': 1, 'priority': 0, 'product_id': 0}),
    }
    return role_page.get(role, '')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def changepwd_done(request):
    return render(request, 'changepwd-done.html')


class ChangepwdView(TemplateView):
    template_name = 'changepwd.html'

    def get_context_data(self, **kwargs):
        context = super(ChangepwdView, self).get_context_data(**kwargs)
        context['old_pwd'] = self.request.POST.get('old-pwd', '')
        context['new_pwd'] = self.request.POST.get('new-pwd', '')
        context['new_pwd_again'] = self.request.POST.get('new-pwd-again', '')
        return context

    def post(self, request):
        context = self.get_context_data()

        if not all((context['old_pwd'], context['new_pwd'], context['new_pwd_again'])):
            messages.info(request, u'填写信息不完整')
            return render(request, self.template_name, context)

        if context['new_pwd'] != context['new_pwd_again']:
            messages.info(request, u'两次输入密码不一样')
            return render(request, self.template_name, context)

        user = request.user
        if user.check_password(context['old_pwd']):
            user.set_password(context['new_pwd'])
            user.save()
            update_session_auth_hash(request, user)  # 修改密码不使session失效,从而退出登录
            return redirect('/accounts/changepwddone/')
        else:
            messages.info(request, u'原始密码不正确')
            return render(request, self.template_name, context)

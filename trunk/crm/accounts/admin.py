# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Zone, Role, UserCredit


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


# Define an inline admin descriptor for UserCredit model
class UserCreditInline(admin.StackedInline):
    model = UserCredit
    can_delete = False
    verbose_name_plural = u'附加信息'


# Define a new User admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserCreditInline,)
    list_display = ('username', 'first_name', 'role', 'zone', 'email', 'is_staff')
    ordering = ('username',)
    list_filter = ('is_staff', 'usercredit__role__role', 'usercredit__zone__name')

    def role(self, obj):
        return obj.usercredit.role.role
    role.short_description = u'角色'

    def zone(self, obj):
        return obj.usercredit.zone.name
    zone.short_description = u'大区'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

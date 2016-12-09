# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    role = models.CharField(max_length=32)

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色列表'
        ordering = ['role']

    def __unicode__(self):
        return self.role


class Zone(models.Model):
    name = models.CharField(max_length=32)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = u'大区'
        verbose_name_plural = u'大区列表'
        ordering = ['order']

    @classmethod
    def zone_use(cls):
        return cls.objects.exclude(name=u'全国').all()

    def __unicode__(self):
        return self.name


class UserCredit(models.Model):
    PRIVILEGE_CHOICES = (
        (0, u'普通'),
        (1, u'高级'),
        (2, u'超级'),
    )
    user = models.OneToOneField(User)
    role = models.ForeignKey(Role)
    zone = models.ForeignKey(Zone) 
    privilege = models.IntegerField(choices=PRIVILEGE_CHOICES, default=0, verbose_name=u'权限等级')
    cid = models.CharField(max_length=128, verbose_name=u'客户端cid',default="")
    test_flag = models.BooleanField(default=False, verbose_name=u'测试账号标记')

    class Meta:
        verbose_name = u'百融用户'
        ordering = ['id']

    def get_products(self):
        return ','.join(self.product_set.all().values_list('name', flat=True))

    def project_count_list(self):
        progress_val = [project.get_cur_progress_val() for project in self.project_set.all()]
        return [progress_val.count(p) for p in xrange(1, 7)]

    def __unicode__(self):
        return self.user.get_full_name()

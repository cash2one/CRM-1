# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import collections
import datetime

from django.db import models

from jsonfield.fields import JSONField
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

from accounts.models import Zone, UserCredit

class CustomerType(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'客户类型')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'客户类型'
        verbose_name_plural = u'客户类型列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class CustomerCategory1(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'一级类目名称')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'客户一级类目'
        verbose_name_plural = u'客户一级类目列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class CustomerCategory2(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'二级类目名称')
    category1 = models.ForeignKey(CustomerCategory1, verbose_name=u'关联一级类目')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'客户二级类目'
        verbose_name_plural = u'客户二级类目列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class CustomerCategory3(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'三级类目名称')
    category2 = models.ForeignKey(CustomerCategory2, verbose_name=u'关联二级类目')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'客户三级类目'
        verbose_name_plural = u'客户三级类目列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Customer(models.Model):

    PRIORITY_CHOICES = (
        (1, u'公司级重点客户'),
        (2, u'区域级重点客户'),
        (3, u'非重点客户'),
    )

    name = models.CharField(max_length=128, verbose_name=u'客户全称')
    short_name = models.CharField(max_length=64, verbose_name=u'客户简称')
    type = models.ForeignKey(CustomerType, verbose_name=u'客户类型')
    category1 = models.ForeignKey(CustomerCategory1, blank=True, null=True, verbose_name=u'客户一级类目')
    category2 = models.ForeignKey(CustomerCategory2, blank=True, null=True, verbose_name=u'客户二级类目')
    category3 = models.ForeignKey(CustomerCategory3, blank=True, null=True, verbose_name=u'客户三级类目')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3, verbose_name=u'客户级别')
    zone = models.ForeignKey(Zone, verbose_name=u'区域')
    province = models.CharField(max_length=64, verbose_name=u'省份')
    city = models.CharField(max_length=64, verbose_name=u'城市')
    address = models.CharField(max_length=255, blank=True, verbose_name=u'详细地址')
    businessman = models.ManyToManyField(UserCredit, verbose_name=u'跟进商务')
    registered_capital = models.IntegerField(verbose_name=u'注册资本')
    shareholder = models.CharField(max_length=128, verbose_name=u'股东')
    product_desc = models.TextField(verbose_name=u'客户业务或产品描述')
    notes = models.TextField(blank=True, verbose_name=u'备注')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')

    class Meta:
        verbose_name = u'客户'
        verbose_name_plural = u'客户列表'
        ordering = ['-timestamp']

    def get_businessmans_name(self):
        return ','.join(self.businessman.all().values_list('user__first_name', flat=True))
    def get_businessmans_zone_name(self):
        return ','.join(self.businessman.all().values_list('zone__name', flat=True))

    def get_projects_name(self):
        return ','.join(self.project_set.filter(is_delete=False).values_list('name', flat=True))

    def get_absolute_url(self):
        return '/crm/customer/view/%i' % self.id

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    order = models.IntegerField(default=0, verbose_name=u'顺序')
    manager = models.ManyToManyField(UserCredit, verbose_name=u'产品负责人', limit_choices_to={'role__role': u'运营经理'})
    imp_apply_define = JSONField(
        blank=True, verbose_name=u'交付申请form定义',
        default={'account': {'label': u'', 'type': 'text', 'value': '', 'required': False, 'initial': ''}}
    )
    mark = models.CharField(max_length=32, verbose_name=u'代号')

    class Meta:
        verbose_name = u'产品'
        verbose_name_plural = u'产品列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'姓名')
    position = models.CharField(max_length=50, verbose_name=u'职位', blank=True)
    tel = models.CharField(max_length=20, blank=True, verbose_name=u'固话')
    mobile = models.CharField(max_length=20, blank=True, verbose_name=u'手机')
    email = models.EmailField(blank=True, verbose_name=u'邮箱')
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')

    class Meta:
        verbose_name = u'联系人'
        verbose_name_plural = u'联系人列表'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'项目名称')
    customer = models.ForeignKey(Customer)
    products = models.ManyToManyField(Product)
    notes = models.TextField(blank=True, verbose_name=u'备注')
    businessman = models.ManyToManyField(UserCredit, verbose_name=u'商务')
    contacts = models.ManyToManyField(Contact, blank=True, verbose_name=u'联系人')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')
    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目列表'
        ordering = ['-timestamp']

    @property
    def priority(self):
        return self.customer.priority

    @property
    def priority_display(self):
        return self.customer.get_priority_display()

    def get_state(self):
        if not self.progress_set.exists():
            return u'沉默'
        progress = self.progress_set.latest('timestamp')
        day = (datetime.date.today() - progress.timestamp.date()).days
        if day <= 3:
            state = u'活跃'
        elif 3 < day <= 7:
            state = u'稳定'
        else:
            state = u'沉默'
        return state

    def del_enabled(self):
        """如果项目有未处理完的订单,则不能删除的"""
        return not (self.testapply_set.filter(state=False).exists() or self.impapply_set.filter(state=False).exists())

    def get_products_name(self):
        return ','.join(self.products.all().values_list('name', flat=True))

    def get_businessmans_name(self):
        return ','.join(self.businessman.all().values_list('user__first_name', flat=True))

    def get_contacts_name(self):
        return ','.join(self.contacts.all().values_list('name', flat=True))

    def get_latest_progress(self):
        """
        获取最新的进度progress实例
        最新进度的认定规则：updatetime, timestamp次之
        """
        if not self.progress_set.exists():
            return None
        return self.progress_set.order_by('updatetime', 'timestamp').last()

    def get_cur_progress(self):
        """最新进度的信息"""
        progress = {'progress': '', 'progress_val': 1, 'desc': '', 'plan': '', 'id': ''}
        latest_p = self.get_latest_progress()
        if latest_p:
            progress['progress'] = latest_p.get_progress_display()
            progress['progress_val'] = latest_p.progress
            progress['desc'] = latest_p.description
            progress['plan'] = latest_p.plan
            progress['id'] = latest_p.id
        return progress

    def get_latest_progress_updatetime(self):
        latest_p = self.get_latest_progress()
        if latest_p:
            return latest_p.updatetime
        else:
            return 0

    def get_cur_progress_val(self):
        latest_p = self.get_latest_progress()
        if latest_p:
            return latest_p.progress
        else:
            return 1

    def get_mark_content(self):
        progress = self.get_latest_progress()
        if progress:
            progress_id = progress.id
            if Mark.objects.filter(progress__id=progress_id).exists():
                mark = Mark.objects.get(progress__id=progress_id)
                return mark.content
            else:
                return ''
        else:
            return ''

    def get_absolute_url(self):
        return '/crm/project/view/%i' % self.id

    def __unicode__(self):
        return self.name


class Progress(models.Model):

    PROGRESS_CHOICES = (
        (1, u'准备'),
        (2, u'接洽'),
        (3, u'测试/试用'),
        (4, u'谈判'),
        (5, u'上线'),
        (6, u'售后'),
    )
    PTYPE = (
        (0, u'常规'),
        (1, u'测试'),
        (2, u'交付'),
    )

    ptype = models.IntegerField(choices=PTYPE, default=0)
    project = models.ForeignKey(Project)
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=1)
    description = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    updatetime = models.DateField(default='1980-01-01')
    operator = models.CharField(max_length=32, verbose_name=u'更新人')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'进度'
        verbose_name_plural = u'进度列表'
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return '/progress/view/%i' % self.id

    def __unicode__(self):
        return self.get_progress_display()


class TestResult(models.Model):
    name = models.CharField(max_length=64)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = u'测试结果要求'
        verbose_name_plural = u'测试结果要求列表'
        ordering = ['order']

    def __unicode__(self):
        return self.name


class TestApply(models.Model):

    PROGRESS_CHOICES = (
        (1, u'待测试'),
        (2, u'测试中'),
        (3, u'测试完成'),
        (4, u'退回'),
    )

    applyman = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'商务'},
            related_name='testapply_applyman_set', verbose_name=u'申请人'
    )
    project = models.ForeignKey(Project)
    dts_account = models.CharField(max_length=64, verbose_name=u'dts账号')
    analyser = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'风控经理'},
            related_name='testapply_analser_set'
    )
    amount_data = models.PositiveIntegerField(verbose_name=u'测试数据量')
    goal = models.TextField(verbose_name=u'本次测试目标')
    test_fields = models.CharField(max_length=255, verbose_name=u'客户提供的测试字段')
    test_result = models.ManyToManyField(TestResult, verbose_name=u'测试结果要求')
    overdue_state = models.BooleanField(verbose_name=u'是否提供逾期状态', default=False)
    notes = models.TextField(blank=True, verbose_name=u'备注')
    state = models.BooleanField(verbose_name=u'测试完成', default=False)
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=1, verbose_name=u'当前阶段')
    modify_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')
    # on_delete=models.SET_NULL 当外连的contact被删除时, 将这里的contact设置为null,否则会一起被删除
    contact = models.ForeignKey(Contact, verbose_name=u'联系人', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = u'测试申请'
        verbose_name_plural = u'测试申请列表'
        ordering = ['-create_time']

    def get_customer_name(self):
        return self.project.customer.name

    def get_test_result(self):
        return ', '.join([ts.name for ts in self.test_result.all()])

    def get_overdue_state(self):
        return u'是' if self.overdue_state else u'否'

    def get_state(self):
        return u'测试完成' if self.state else self.project.get_test_progress_display()

    def get_latest_progress(self):
        return self.testapplyprogress_set.latest('timestamp')

    def get_absolute_url(self):
        return '/crm/test-apply/view/%i' % self.id

    def get_edit_url(self):
        return '/crm/test-apply/edit/view/%i' % self.id

    def get_del_url(self):
        return '/crm/test-apply/del/%i' % self.id

    def get_progress_add_url(self):
        return '/crm/test-apply/progress/add/%i' % self.id

    def __unicode__(self):
        return '%s test apply' % self.project.name


class TestApplyProgress(models.Model):

    PROGRESS_CHOICES = (
        (1, u'待测试'),
        (2, u'测试中'),
        (3, u'测试完成'),
        (4, u'退回'),
    )

    test_apply = models.ForeignKey(TestApply)
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=1, verbose_name=u'进度')
    description = models.TextField(blank=True, verbose_name=u'描述')
    operator = models.CharField(max_length=32, verbose_name=u'更新人')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')

    class Meta:
        verbose_name = u'测试申请进度'
        verbose_name_plural = u'测试申请进度列表'
        ordering = ['-timestamp']

    def __unicode__(self):
        return '%s test apply progress' % self.test_apply.project.name


class DataModule(models.Model):

    name = models.CharField(max_length=128, verbose_name=u'模块名称')
    code = models.CharField(max_length=255)
    category = models.CharField(max_length=128, verbose_name=u'类别')
    status = models.BooleanField(default=False, verbose_name=u'状态')

    class Meta:
        verbose_name = u'数据模块'
        verbose_name_plural = u'数据模块列表'

    @classmethod
    def get_category_list(cls):
        """获取数据模块的类别"""
        category_list = cls.objects.all().values_list('category', flat=True)
        # 保持顺序去重
        new_list = []
        for category in category_list:
            if category not in new_list:
                new_list.append(category)
        return new_list

    @classmethod
    def get_data_dict(cls):
        """
        用OrderedDict存储数据
        key: category
        value: 是datamodule列表,属于key的分类
        """
        category_list = cls.get_category_list()
        data_dict = collections.OrderedDict()
        for category in category_list:
            data_dict[category] = cls.objects.filter(category=category).all()
        return data_dict

    def __unicode__(self):
        return self.name


class HNApiProduct(models.Model):

    name = models.CharField(max_length=128, verbose_name=u'产品名称')
    code = models.CharField(max_length=255)
    category = models.CharField(max_length=128, verbose_name=u'类别')
    status = models.BooleanField(default=False, verbose_name=u'状态')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'海纳API产品'
        verbose_name_plural = u'海纳API产品列表'
        ordering = ['order']

    @classmethod
    def get_category_list(cls):
        """获取数据模块的类别"""
        category_list = cls.objects.filter(status=True).all().values_list('category', flat=True)
        # 保持顺序去重
        new_list = []
        for category in category_list:
            if category not in new_list:
                new_list.append(category)
        return new_list

    @classmethod
    def get_data_dict(cls):
        """用OrderedDict存储数据
        key: category
        value: 是datamodule列表,属于key的分类
        """
        category_list = cls.get_category_list()
        data_dict = collections.OrderedDict()
        for category in category_list:
            data_dict[category] = cls.objects.filter(status=True, category=category).all()
        return data_dict

    def __unicode__(self):
        return self.name


class ImpApply(models.Model):

    ACCOUNT_TYPE_CHOICES = (
        (1, u'测试'),
        (2, u'正式'),
    )
 
    PROGRESS_CHOICES = (
        (9, u'二次提交'),
        (10, u'待提交'),
        (11, u'风控经理退回'),
        (12, u'运营经理退回'),
        (13, u'交付经理退回'),
        (20, u'待风控经理审核'),
        (30, u'待运营经理审核'),
        (40, u'待交付'),
        (44, u'交付指回'),
        (45, u'开通账号中'),
        (46, u'开通账号'),
        (47, u'解析完成'),
        (48, u'接口调通'),
        (49, u'已转正'),
        (50, u'交付完成'),
    )

    applicant = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'商务'},
            related_name='impapply_applicant_set', verbose_name=u'申请人'
    )
    analyser = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'风控经理'}, blank=True, null=True,
            related_name='impapply_analser_set', verbose_name=u'风控经理'
    )
    operations = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'运营经理'}, blank=True, null=True,
            related_name='impapply_operations_set', verbose_name=u'运营经理'
    )
    imp_engineer = models.ForeignKey(
            UserCredit, limit_choices_to={'role__role': u'交付总监','role__role': u'交付经理'},
            related_name='impapply_imp_engineer_set', verbose_name=u'交付经理'
    )
    project = models.ForeignKey(Project)
    product = models.ForeignKey(Product)
    extra_fields = JSONField(blank=True, verbose_name=u'附加字段值')
    contact = models.ForeignKey(Contact, blank=True, null=True, verbose_name=u'联系人', on_delete=models.SET_NULL)
    pic = ThumbnailerImageField(upload_to='email_pic', blank=True, null=True, verbose_name=u'邮件确认截图')
    notes = models.TextField(blank=True, verbose_name=u'备注')
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=30, verbose_name=u'当前阶段')
    state = models.BooleanField(default=False, verbose_name=u'交付完成')
    modify_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')

    class Meta:
        verbose_name = u'交付申请'
        verbose_name_plural = u'交付申请列表'
        ordering = ['-modify_time']

    def __getattr__(self, item):
        try:
            return self.extra_fields[item]
        except KeyError:
            raise AttributeError

    def set_extra_field(self, field_name, value):
        self.extra_fields[field_name] = value

    def get_done_time_display(self):
        extra_fields = self.extra_fields
        if 'done_time' in extra_fields:
            done_time_items = {0: u'30天', 1: u'60天', 2: u'90天', 3: u'180天', 4: u'无限制（正式账号）'}
            done_time = extra_fields['done_time']
            # TODO 这是为了解决遗留数据的问题
            if isinstance(done_time, dict):
                done_time = int(done_time.get('value', 0))
            return done_time_items.get(done_time, '')
        else:
            return ''

    def get_latest_progress(self):
        return self.impapplyprogress_set.latest('create_time')

    def get_account_type_display(self):
        return u'测试' if self.extra_fields['account_type'] == '1' else u'正式'

    def get_multi_apply_display(self):
        return u'否' if self.extra_fields['multi_apply'] == '否' else u'是'

    def get_absolute_url(self):
        return '/crm/imp-apply/view/%i' % self.id

    def get_pic_url(self):
        return get_thumbnailer(self.pic)['avatar'].url

    def get_edit_url(self):
        return '/crm/imp-apply/edit/%i' % self.id

    def get_del_url(self):
        return '/crm/imp-apply/del/%i' % self.id

    def get_progress_add_url(self):
        return '/crm/imp-apply/progress/add/%i' % self.id

    def get_free_date_start_edit_url(self):
        return '/crm/imp-apply/free-date-start/edit/%i' % self.id

    def __unicode__(self):
        return '%s imp-apply' % self.product.name


class ImpApplyProgress(models.Model):

    imp_apply = models.ForeignKey(ImpApply)
    progress = models.IntegerField(choices=ImpApply.PROGRESS_CHOICES, default=10, verbose_name=u'进度')
    description = models.TextField(blank=True, verbose_name=u'描述')
    operator = models.CharField(max_length=32, verbose_name=u'更新人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'删除')

    class Meta:
        verbose_name = u'交付申请进度'
        verbose_name_plural = u'交付申请进度列表'
        ordering = ['-create_time']

    def __unicode__(self):
        return '%s: %s imp apply' % (self.imp_apply.project.name, self.imp_apply.product.name)


class Mark(models.Model):
    usercredit = models.ForeignKey(UserCredit)
    progress = models.OneToOneField(Progress)
    content = models.TextField()
    updatetime = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'标注'
        verbose_name_plural = u'标注列表'
        ordering = ['-timestamp']

    def __unicode__(self):
        return 'Mark--id: %s user: %s datetime: %s' % (self.id, self.usercredit.user.first_name, self.timestamp)


class Config(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    value = models.CharField(max_length=255, verbose_name=u'值')
    description = models.TextField(blank=True, verbose_name=u'描述')
    modify_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'配置信息'
        verbose_name_plural = u'配置列表'

    def __unicode__(self):
        return 'System Config: %s' % self.name


class JsonConfig(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    value = JSONField(blank=True, verbose_name=u'值')
    description = models.TextField(blank=True, verbose_name=u'描述')
    modify_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'Json配置信息'
        verbose_name_plural = u'Json配置信息列表'

    def __unicode__(self):
        return 'Json Config: %s' % self.name


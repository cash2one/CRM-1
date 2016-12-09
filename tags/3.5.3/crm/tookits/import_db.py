# -*- coding: utf-8 -*-

"""数据导入"""

import os
import sys
import xlrd
from readxls import read_xls
from django.contrib.auth.models import User
from crm.models import Customer, CustomerType, Project, Contact, Progress, Product
from accounts.models import UserCredit, Zone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")

# Django 版本>=1.7时，需要加下面两句,否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
import django
if django.VERSION >= (1, 7):
    django.setup()


PRIORITY = ('高', '中', '低')
PROGRESS_CHOICES = ('准备', '接洽', '测试/试用', '谈判', '上线', '售后')


def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]


def read_data(path):
    name = get_basename(path)
    book = xlrd.open_workbook(path)
    print '读取<%s>的客户表......' % name
    customers = read_xls(book, u'客户')
    print 'done!'
    print '读取<%s>的项目表......' % name
    projects = read_xls(book, u'项目')
    print 'done!'
    print '读取<%s>的进度表......' % name
    progresses = read_xls(book, u'进度')
    print 'done!'
    print '读取<%s>的联系人表......' % name
    contacts = read_xls(book, u'联系人')
    print 'done!'
    return (customers, projects, progresses, contacts)


def check_user(name):
    print '验证用户<%s>是否存在......' % name
    if User.objects.filter(first_name=name).exists():
        user = User.objects.get(first_name=name)
        usercredit = UserCredit.objects.get(user=user)
        print 'correct!'
        return True, usercredit
    else:
        print '用户<%s>不存在!' % name
        return False, None


def import_customers(customers, name, usercredit):
    print '开始导入<%s>的客户数据......' % name
    for c in customers:
        print '导入客户<%s>......' % c[0]
        if not Customer.objects.filter(name=c[0]).exists():
            # 如果客户不存在，创建客户实例
            try:
                customer = Customer(name=c[0],
                                    type=CustomerType.objects.get(name=c[1]),
                                    priority=PRIORITY.index(c[2])+1,
                                    zone=Zone.objects.get(name=c[3]),
                                    province=c[4],
                                    city=c[5],
                                    address=c[6],
                                    notes=c[7]
                                    )
                customer.save()
                customer.businessman.add(usercredit)
                print 'done'
            except Exception, e:
                print e
                cmd = raw_input('导入客户<%s>时发生异常, 是否继续? yes/no' % c[0])
                if cmd=='no':sys.exit()
        else:
            # 如果该客户已经存在，并且当前商务也不在该客户的跟进商务里，那么就把当前商务添加到跟进商务里
            print '客户<%s>已经存在' % c[0]
            customer = Customer.objects.get(name=c[0], is_delete=False)
            if usercredit not in customer.businessman.all():
                customer.businessman.add(usercredit)
    print '<%s>的客户数据导入完成' % name


def import_projects(projects, name, usercredit):
    print '开始导入<%s>的项目数据......' % name
    for p in projects:
        print '导入项目<%s>......' % p[0]
        if not Project.objects.filter(name=p[0], is_delete=False).exists():
            try:
                project = Project(name=p[0],
                                  customer=Customer.objects.get(name=p[1]),
                                  product=Product.objects.get(name=p[2]),
                                  priority=PRIORITY.index(p[3])+1,
                                  notes=p[4]
                                  )
                project.save()
                project.businessman.add(usercredit)
            except Exception, e:
                print e
                cmd = raw_input('导入项目<%s>时发生异常, 是否继续? yes/no' % p[0])
                if cmd=='no':sys.exit()
        else:
            print '项目<%s>已经存在' % p[0]
            project = Project.objects.get(name=p[0], is_delete=False)
            if usercredit not in project.businessman.all():
                project.businessman.add(usercredit)
    print '<%s>的项目数据导入完成' % name


def import_progresses(progresses, name, usercredit):
    print '开始导入<%s>的进度数据......' % name
    for p in progresses:
        if Project.objects.filter(name=p[0], is_delete=False).exists():
            project = Project.objects.get(name=p[0], is_delete=False)
            if usercredit not in project.businessman.all():
                print '<%s>不在项目<%s>的跟进商务里!' % (name, p[0])
                continue
            try:
                progress = Progress(project=project,
                                    progress=PROGRESS_CHOICES.index(p[1])+1,
                                    description=p[2],
                                    plan=p[3],
                                    updatetime=p[4],
                                    operator=name
                                    )
                progress.save()
            except Exception, e:
                print e
                cmd = raw_input('导入进度<%s>时发生异常, 是否继续? yes/no' % p[1])
                if cmd=='no':sys.exit()
        else:
            print '项目<%s>不存在' % p[0]
    print '<%s>的进度数据导入完成' % name


def import_contacts(contacts, name, usercredit):
    print '开始导入<%s>的联系人数据......' % name
    for c in contacts:
        # 如果项目存在，并且项目中没有同名的联系人，那么新建联系人并加到项目中
        if Project.objects.filter(name=c[0], is_delete=False).exists():
            project = Project.objects.get(name=c[0], is_delete=False)
            if usercredit not in project.businessman.all():
                print '<%s>不在项目<%s>的跟进商务里!' % (name, c[0])
                continue
            if not project.contacts.all().filter(name=c[1]).exists():
                contact = Contact(name=c[1],
                                  position=c[2],
                                  tel=c[3],
                                  mobile=c[4],
                                  email=c[5]
                                  )
                contact.save()
                project.contacts.add(contact)
        else:
            print '项目<%s>不存在!' % c[0]


if __name__ == "__main__":
    dirname = '/home/baixue/100credit/CRMData/now/'
    for filename in os.listdir(dirname):
        path = os.path.join(dirname, filename)
        # 去掉扩展名
        name = os.path.splitext(filename)[0]
        print '-----------------------处理xls文件-----------------------'
        print '开始处理<%s>的文件......' % name
        datas = read_data(path)
        print '读取数据完成!'
        print '------------------------验证用户-------------------------'
        status, usercredit = check_user(name)
        if not status:continue
        print '-----------------------开始导入数据-----------------------'
        customers, projects, progresses, contacts = datas
        import_customers(customers, name, usercredit)
        print
        import_projects(projects, name, usercredit)
        print
        import_progresses(progresses, name, usercredit)
        print
        import_contacts(contacts, name, usercredit)
        print '<%s>的数据导入完成!' % name

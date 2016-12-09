# -*- coding: utf-8 -*-

from django import template

from ..models import Progress, Mark


register = template.Library()


@register.filter
def get_dict_price(d, k):
    try:
        return d[k]['price']
    except KeyError:
        return ''
    except Exception:
        return 'XXXXXXXX'


@register.filter
def get_dict_val(d, k):
    try:
        return d[k]['val']
    except KeyError:
        return ''
    except Exception:
        return 'XXXXXXXX'


@register.filter
def get_dict_note(d, k):
    try:
        return d[k]['note']
    except KeyError:
        return ''
    except Exception:
        return 'XXXXXXXX'


@register.filter
def project_count(projects, progress):
    """根据进度代号判断,统计给定项目中处在该进度期的项目个数"""
    return [project.get_cur_progress_val() for project in projects].count(progress)


@register.filter
def project_count_(businessman, progress):
    """根据进度代号判断,统计给定商务的项目处在该进度期的个数"""
    Progress.objects.filter(project__businessman=businessman).raw(
            'SELECT COUNT(*) FROM blog_entry WHERE FROM GROUP BY project'
    )
    return


@register.filter
def get_project_progress(project, args):
    """获取项目进度的最新"""
    if not project.progress_set.exists():
        return ''
    if args == 'progress':
        return project.progress_set.latest('updatetime').get_progress_display()
    elif args == 'desc':
        return project.progress_set.latest('updatetime').description
    elif args == 'plan':
        return project.progress_set.latest('updatetime').plan
    elif args == 'id':
        return project.progress_set.latest('updatetime').id
    else:
        return ''


@register.filter
def get_mark_content(project):
    if not project.progress_set.exists():
        return ''
    progress_id = project.progress_set.latest('updatetime').id
    if Mark.objects.filter(progress__id=progress_id).exists():
        return Mark.objects.get(progress__id=progress_id).content
    else:
        return ''

#-*- coding:utf-8 -*-
#Author: Guangjie Guo


from django import template
from vpn.api import *

register = template.Library()


@register.filter(name='members_count')
def members_count(group_id):
    """统计用户组下成员数量"""
    group = get_object(Depa, id=group_id)
    if group:
        return group.useinfo_set.count()
    else:
        return 0

@register.filter(is_safe=False)
def length(value):
    """Returns the length of the value - useful for lists."""
    try:
        return len(value)
    except (ValueError, TypeError):
        return 0




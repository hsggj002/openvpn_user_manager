#-*- coding:utf-8 -*-
#Author: Guangjie Guo
# coding:utf-8
# import urllib
# import urllib2
import json,re
import ssl



from django.core.paginator import Paginator, EmptyPage, InvalidPage




def page_list_return(total, current=1):
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page+1)


def pages(posts, r):
    """分页公用函数"""
    contact_list = posts
    print(contact_list,'=----------->')
    p = paginator = Paginator(contact_list, 10)
    try:
        current_page = int(r.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(p.page_range), current_page)
    print(page_range)

    try:
        contacts = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0
    if current_page <= (len(p.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    print(contact_list, p, contacts, page_range, current_page, show_first, show_end)
    print('contact_list, p, contacts, page_range, current_page, show_first, show_end')
    return contact_list, p, contacts, page_range, current_page, show_first, show_end







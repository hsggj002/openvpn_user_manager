# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from vpngroup import views

urlpatterns = [
    url(r'^group_list/$', views.group_list,name='group_list'),
    url(r'^add_group/$', views.add_group,name='add_group'),
    url(r'^g_edit-id=(\d+)$', views.g_edit,name='g_edit'),
    url(r'^g_delete-id=(\d+)$', views.g_delete,name='g_delete'),
]

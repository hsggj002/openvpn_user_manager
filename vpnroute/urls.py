# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from vpnroute import views

urlpatterns = [
    url(r'^route_list/$', views.route_list,name='route_list'),
    url(r'^add_route/$', views.add_route,name='add_route'),
    url(r'^r_edit-id=(\d+)$', views.r_edit,name='r_edit'),
    url(r'^r_delete-id=(\d+)$', views.r_delete,name='r_delete'),
]

# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from vpnnetwork import views

urlpatterns = [
    url(r'^network_list/$', views.network_list, name='network_list'),
    url(r'^add_network/$', views.add_network, name='add_network'),
    url(r'^n_edit-id=(\d+)$', views.network_edit, name='network_edit'),
    url(r'^n_delete-id=(\d+)$', views.network_delete, name='network_delete'),
]

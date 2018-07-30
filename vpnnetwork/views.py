#-*- coding:utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from vpn.models import *
from util.md5 import encrypt
from openvpn.settings import *
from vpnnetwork.api import *
from vpn.api import *
import re,datetime
from django.db.models import Q
import json
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


@auth
def add_network(request):
    if request.method=='GET':
        obj = NetworkForm()
        return render(request,'Onetwork/add_network.html',{'obj':obj})
    else:
        obj = NetworkForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)

            Netaddress.objects.create(**obj.cleaned_data)

            return redirect('/vpnnetwork/network_list')
        else:
            print('错误信息',obj.errors)
        return render(request,'Onetwork/add_network.html',{'obj':obj})

@auth
def network_list(request):
    network_list = Netaddress.objects.all().order_by('-id')
    network_id = request.GET.get('id', '')
    keyword = request.GET.get('keyword', '')

    if keyword:
        network_list = network_list.filter(Q(addrname__icontains=keyword) | Q(gw_addrname__icontains=keyword)).order_by('-id')


    network_list, p, networks, page_range, current_page, show_first, show_end = pages(network_list, request)

    # ret = Depa.objects.filter(name='service').values('routemgr__name')
    return render(request,'Onetwork/network_list.html',locals())

@auth
def network_edit(request,nid):
    if request.method=='GET':
        network=Netaddress.objects.filter(id=nid).first()
        obj = NetworkForm(initial={'addrname':network.addrname,'gw_addrname':network.gw_addrname})
        # print(group)
        # print(obj)
        return render(request,'Onetwork/network_edit.html',{'nid':nid,'obj':obj})
    else:
        obj = NetworkForm(data=request.POST)
        # backfile()
        if obj.is_valid():
            Netaddress.objects.filter(id=nid).update(**obj.cleaned_data)


            return redirect('/vpnnetwork/network_list')
        return render(request,'Onetwork/network_edit.html',{'nid':nid,'obj':obj})

@auth
def network_delete(request,nid):
    Netaddress.objects.filter(id=nid).delete()
    return redirect('/vpnnetwork/network_list')
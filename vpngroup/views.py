#-*- coding:utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from vpn.models import *
from util.md5 import encrypt
from openvpn.settings import *
from vpngroup.api import *
from vpn.api import *
import re,datetime
from django.db.models import Q
import json
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


@auth
def add_group(request):
    if request.method=='GET':
        obj = GroupForm()
        return render(request,'Ogroup/add_group.html',{'obj':obj})
    else:
        obj = GroupForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)

            Depa.objects.create(**obj.cleaned_data)

            write_file(obj)

            return redirect('/vpngroup/group_list')
        else:
            print('错误信息',obj.errors)
        return render(request,'Ogroup/add_group.html',{'obj':obj})

@auth
def group_list(request):
    user_group_list = Depa.objects.all().order_by('name')
    group_id = request.GET.get('id', '')
    if group_id:
        user_group_list = user_group_list.filter(id=int(group_id))
    user_group_list, p, user_groups, page_range, current_page, show_first, show_end = pages(user_group_list, request)

    ret = Depa.objects.filter(name='service').values('routemgr__name')
    return render(request,'Ogroup/group_list.html',locals())

@auth
def g_edit(request,nid):
    if request.method=='GET':
        group=Depa.objects.filter(id=nid).first()
        obj = GroupForm(initial={'name':group.name,'comment':group.comment})
        print(group)
        print(obj)
        return render(request,'Ogroup/g_edit.html',{'nid':nid,'obj':obj})
    else:
        obj = GroupForm(data=request.POST)
        # backfile()
        if obj.is_valid():
            Depa.objects.filter(id=nid).update(**obj.cleaned_data)

            write_file(obj)

            return redirect('/vpngroup/group_list')
        return render(request,'Ogroup/g_edit.html',{'nid':nid,'obj':obj})

@auth
def g_delete(request,nid):
    Depa.objects.filter(id=nid).delete()
    return redirect('/vpngroup/group_list')
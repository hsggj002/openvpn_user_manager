#-*- coding:utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from vpn.models import *
from util.md5 import encrypt
from openvpn.settings import *
from vpn.api import *
from vpnroute.api import *
from vpngroup.api import *
import re,datetime
from django.db.models import Q
import json
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')



@auth
def route_list(request):
    route_list = Routemgr.objects.all().order_by('name')
    route_id = request.GET.get('id','')
    if route_id:
        route_list = route_list.filter(id=int(route_id))
    route_list, p, routers, page_range, current_page, show_first, show_end = pages(route_list, request)

    return render(request, 'Orouter/route_list.html',locals())

@auth
def add_route(request):
    if request.method=='GET':
        obj = RouteForm()
        return render(request,'Orouter/add_route.html',{'obj':obj})
    else:
        obj = RouteForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)

            Routemgr.objects.create(**obj.cleaned_data)

            return redirect('/vpnroute/route_list')
        else:
            print('错误信息',obj.errors)
        return render(request,'Orouter/add_route.html',{'obj':obj})

@auth
def r_edit(request,nid):
    if request.method=='GET':
        route=Routemgr.objects.filter(id=nid).first()
        obj = RouteForm(initial={'name':route.name,'tactful':route.tactful})
        return render(request,'Orouter/r_edit.html',{'nid':nid,'obj':obj})
    else:
        obj = RouteForm(data=request.POST)
        if obj.is_valid():
            Routemgr.objects.filter(id=nid).update(**obj.cleaned_data)
            # write_file(obj)
            return redirect('/vpnroute/route_list')
        return render(request,'Orouter/r_edit.html',{'nid':nid,'obj':obj})

@auth
def r_delete(request,nid):
    ret = Routemgr.objects.filter(id=nid).values().first()
    ret1 = Routemgr.objects.filter(name=ret['name']).values('depa__name').first()
    ret2=Depa.objects.filter(name=ret1['depa__name']).values('useinfo__account')
    for i in ret2:
        with open('%s%s' %(CCD_PATH,i['useinfo__account']), 'r') as u:
            lines = u.readlines()
        with open('%s%s' %(CCD_PATH,i['useinfo__account']), 'w') as f:
            for i in lines:
                datas = i.strip()
                if len(datas)!=0:
                    if 'route' in i:
                        continue
                    f.write(i + '\n')

    Routemgr.objects.filter(id=nid).delete()
    return redirect('/vpnroute/route_list')
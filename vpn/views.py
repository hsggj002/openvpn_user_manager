#-*- coding:utf-8 -*-


from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from vpn.models import *
from util.md5 import encrypt
from openvpn.settings import *
from vpn.api import *
import re,datetime
from django.db.models import Q
import json
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


@auth
def index(request):
    users = UseInfo.objects.all()

    import time
    r = time.asctime().split(' ')
    user_num=[]
    with open('%sopenvpn-status.log' %LOG_PATH) as f:
        for i in f.readlines():
            ret = i.strip().split(',')
            if "10.100" in ret[0] and (r[1] or r[2] or r[4]) in ret[3]:
                user_num.append(ret)

    r = time.strftime('%Y-%m-%d')
    error_num = []
    with open('%sopenvpn_error.log' %LOG_PATH) as f:
        for i in f.readlines():
            ret = i.strip().split(' ')
            if r in ret:
                error_num.append(error_num)

    return render(request, 'index.html', locals())



@auth
def user_list(request):

    keyword = request.GET.get('keyword', '')
    gid = request.GET.get('gid', '')
    users_list = UseInfo.objects.all().order_by('-id')

    if keyword:
        users_list = users_list.filter(Q(account__icontains=keyword) | Q(name__icontains=keyword)).order_by('account')


    users_list, p, users, page_range, current_page, show_first, show_end = pages(users_list, request)
    print(users.has_previous)

    return render(request,'Ouser/user_list.html',locals())



@auth
def add(request):
    if request.method=='GET':
        obj = UserForm()
        return render(request,'Ouser/add.html',{'obj':obj})
    else:
        # backfile()
        obj = UserForm(request.POST)
        if obj.is_valid():
            '''输入邮箱账号，得到前缀'''
            account_name = obj.cleaned_data['account']
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", account_name) != None:
                obj.cleaned_data['account'] = account_name.split('@')[0]
                group_route = Depa.objects.get(id=obj.cleaned_data['depaer_id'])
                address = Netaddress.objects.filter(id=obj.cleaned_data['address_id'])
                with open("%s%s"%(CCD_PATH,obj.cleaned_data['account']),"w") as f:
                    f.write("%s %s %s\n%s\n" % ("ifconfig-push", address[0].addrname, address[0].gw_addrname, group_route.routemgr.tactful))
                obj.cleaned_data['password']=rand_sec()
                address.update(flag=1)
            send_mail(obj.cleaned_data['account'],obj.cleaned_data['password'],account_name)
            UseInfo.objects.create(**obj.cleaned_data)
            Netaddress.objects.filter(id=obj.cleaned_data['address_id']).update(flag=1)
            return redirect('/user_list')
        else:
            print('错误信息',obj.errors)
        return render(request,'Ouser/add.html',{'obj':obj})

@auth
def edit(request,nid):
    if request.method=='GET':
        user=UseInfo.objects.filter(id=nid).first()
        # Netaddress.objects.filter(id=user.address_id).update(flag=0)
        print(user.address_id)
        obj = UserForm(initial={'name':user.name,'account':user.account,'address_id':user.address_id,'password':user.password,'depaer_id':user.depaer_id})
        return render(request,'Ouser/edit.html',{'nid':nid,'obj':obj})
    else:
        # backfile()
        obj = UserForm(data=request.POST)
        if obj.is_valid():
            user = UseInfo.objects.get(id=nid)
            address = Netaddress.objects.filter(id=obj.cleaned_data['address_id'])
            if os.path.exists("%s%s"%(CCD_PATH,user.account)):
                os.remove("%s%s"%(CCD_PATH,user.account))
            account_name = obj.cleaned_data['account']
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", account_name) != None:
                obj.cleaned_data['account'] = account_name.split('@')[0]
                group_route = Depa.objects.get(id=obj.cleaned_data['depaer_id'])
                with open("%s%s"%(CCD_PATH,obj.cleaned_data['account']),"w") as f:
                    f.write("%s %s %s\n%s\n" % ("ifconfig-push",address[0].addrname,address[0].gw_addrname,group_route.routemgr.tactful))

            UseInfo.objects.filter(id=nid).update(**obj.cleaned_data)
            if user.address_id != obj.cleaned_data['address_id']:
                Netaddress.objects.filter(id=user.address_id).update(flag=0)
                Netaddress.objects.filter(id=obj.cleaned_data['address_id']).update(flag=1)
            return redirect('/user_list')
        return render(request,'Ouser/edit.html',{'nid':nid,'obj':obj})

@auth
def delete(request,nid):
    # backfile()

    user = UseInfo.objects.get(id=nid)
    Netaddress.objects.filter(id=user.address_id).update(flag=0)
    if os.path.exists("%s%s" %(CCD_PATH,user.account)):
        os.remove("%s%s" %(CCD_PATH,user.account))
    user.delete()

    return redirect('/user_list')

@auth
def delete_all(request,nid):
    for i in nid:
        UseInfo.objects.filter(id=i).delete()
    return redirect('/user_list')

@auth
def add_batch(request):

    return render(request, 'Ouser/add_batch.html')

@auth
def user_mgr(request):

    return render(request,'Ouser/add_batch.html')


@auth
def write_out(request):
    dic = {'flag':False}
    dic['flag']=True
    write_outfile()
    return HttpResponse(json.dumps(dic))

@auth
def logout(request):
    request.session.clear()
    return redirect('/login')





























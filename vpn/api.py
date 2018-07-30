#-*- coding:utf-8 -*-
#Author: Guangjie Guo

from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

from django import forms
from django.forms import fields
from django.forms import widgets

from vpn.models import *
from vpnnetwork.api import *
from openvpn.settings import *

import mimetypes
import random
import os
import xlwt
import logging
import time
import json
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def acc_login(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            # login(request,user)
            request.session['yyyyyyy'] = username
            return redirect('/index')
            # return redirect(request.GET.get('next') or '/')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误'})

def auth(func):
    def inner(request,*args,**kwargs):
        ck = request.session.get('yyyyyyy')
        if not ck:
            return redirect('/login')
        return func(request,*args,**kwargs)
    return inner




class UserForm(forms.Form):
    name = fields.CharField(
        required=False,
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )

    account = fields.EmailField(
        required=True,
        error_messages={'required': '邮箱账号不能为空','invalid': '邮箱格式错误'},
        widget=widgets.EmailInput(attrs={'class': 'form-control','style':'width: 60%;'})
    )

    password = fields.CharField(
        required=False,
        error_messages={'required':'密码不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )


    address_id = fields.IntegerField(
        required=False,
        widget=widgets.Select(
            attrs={'class': 'form-control', 'style': 'width: 60%;'},
            choices=[]
        )
    )


    depaer_id=fields.IntegerField(
        required=True,
        widget=widgets.Select(
            attrs={'class':'form-control','style':'width: 60%;'},
            choices=[]
        )
    )

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields['depaer_id'].widget.choices=Depa.objects.values_list('id','name')
        self.fields['address_id'].widget.choices=Netaddress.objects.filter(flag=0).values_list('id','addrname')





def send_mail(name, password1, mail):
    from_addr = MAIL_ACCOUNT
    password = MAIL_PASSWORD
    to_addr = mail
    smtp_server = 'smtp.263.net'

    mail_msg = u"""
        <p>您好，</p><p>您的openvpn账号已开通，信息如下：</p>
        <p>用户名: %s</p><p>密码: %s</p></br><p>vpn客户端下载地址：</p>
        <p><a href="openvpn-install-2.4.3-I601.exe">windows系统（3.29 MB）</a></p>
        <p><a href="Tunnelblick_3.7.1b_build4813.dmg">mac系统（11.44 MB）</a></p>
        <p>安装及使用方法请查看附件；</p>
        <p>特别提醒：windows版每次运行都需要以管理员身份运行!</p></br>
        <p>本邮件由系统自动发送，请勿直接回复。</p>
        <p>如需帮助，请与运维部联系！</p>
        <p>技术支持：hsggj@com.cn</p>
    """ % (name, password1)

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header(u'您的到家内网 VPN账号已开通（请勿回复本邮件）', 'utf-8').encode()
    msg['X-Priority'] = '2'

    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    names = ['daojia.ovpn', u'VPN-Windows客户端安装说明.pdf', u'VPN-MAC客户端安装使用说明.pdf']


    for file in names:
        basename = os.path.basename(file).encode('utf-8')
        ctype, encoding = mimetypes.guess_type(file)

        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split('/', 1)

        fp = open(file, 'rb')
        mime = MIMEBase(maintype, subtype)
        mime.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(mime)

        mime.add_header('Content-Disposition', 'attachment', filename=('utf-8', 'fr', basename))
        msg.attach(mime)


    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    # print("用户创建成功，邮件已发送至用户邮箱..." + mail)

def rand_sec():
    checkcode = ''

    for i in range(8):
        current = random.randrange(0, 8)
        num = random.randint(65, 122)
        if current != i and num not in range(91, 97):
            temp = chr(num)
        else:
            temp = random.randint(0, 9)

        checkcode += str(temp)

    return checkcode

def get_object(model, **kwargs):
# def get_object(model):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object

def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    paginator = Paginator(post_objects, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end

class LoggerHelper(object):
    _i = None

    @classmethod
    def instance(cls):
        if cls._i:
            return cls._i
        else:
            cls._i = LoggerHelper() #LoggerHelper()
            return cls._i # obj

    def __init__(self):
        error_log = logging.FileHandler('%s/openvpn_error.log' %LOG_PATH, 'a+', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
        error_log.setFormatter(fmt)
        # 创建日志对象
        error_logger = logging.Logger('error', level=logging.INFO)
        # 日志对象和文件对象创建关系
        error_logger.addHandler(error_log)
        self.error_logger = error_logger

        run_log = logging.FileHandler('%s/openvpn_run.log' %LOG_PATH, 'a+', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
        run_log.setFormatter(fmt)
        # 创建日志对象
        run_logger = logging.Logger('run', level=logging.INFO)
        # 日志对象和文件对象创建关系
        run_logger.addHandler(run_log)
        self.run_logger = run_logger


def write_outfile():
    data = xlwt.Workbook()
    table = data.add_sheet('openvpn',cell_overwrite_ok=True)
    ret = UseInfo.objects.filter().values_list()
    table.write(0, 0, u'ID')
    table.write(0, 1, u'账号')
    table.write(0, 2, u'密码')
    table.write(0, 3, u'姓名')
    table.write(0, 4, u'地址')
    table.write(0, 5, u'网关')
    table.write(0, 6, u'组名')
    for k, v in enumerate(ret):
        table.write(k + 1, 0, u'%s' % v[0])
        table.write(k + 1, 1, u'%s' % v[1])
        table.write(k + 1, 2, u'%s' % v[2])
        table.write(k + 1, 3, u'%s' % v[3])
        if v[4]!=None:
            net = Netaddress.objects.get(id=v[4])
            table.write(k + 1, 4, u'%s' % net.addrname)
            table.write(k + 1, 5, u'%s' % net.gw_addrname)
        table.write(k + 1, 6, u'%s' % v[5])
    data.save('%s/static/files/excels/openvpn.xls' %BASE_DIR)

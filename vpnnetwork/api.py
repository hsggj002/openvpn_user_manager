# -*- coding:utf-8 -*

from django import forms
from django.forms import fields
from django.forms import widgets
from vpnnetwork.models import *
from openvpn.settings import *

class NetworkForm(forms.Form):
    addrname = fields.GenericIPAddressField(
        required=True,
        error_messages={'required': '地址不能为空','invalid': '必须输入ipv4地址'},
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )

    gw_addrname = fields.GenericIPAddressField(
        required=True,
        error_messages={'required': '网关不能为空','invalid': '必须输入ipv4地址'},
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )
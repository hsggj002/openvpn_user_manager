# -*- coding:utf-8 -*-

from django import forms
from django.forms import fields
from django.forms import widgets
from vpn.models import *
from openvpn.settings import *

class GroupForm(forms.Form):
    name = fields.CharField(
        required=True,
        error_messages={'required': '组名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )

    comment = fields.CharField(
        required=False,
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )

    routemgr_id = fields.IntegerField(
        required=False,
        widget=widgets.Select(
            attrs={'class':'form-control','style':'width: 60%;'},
            choices=[]
        )
    )

    def __init__(self,*args,**kwargs):
        super(GroupForm,self).__init__(*args,**kwargs)
        self.fields['routemgr_id'].widget.choices=Routemgr.objects.values_list('id','name')



def write_file(obj):
    ret = Depa.objects.filter(name=obj.cleaned_data['name']).values('routemgr__tactful').first()
    ret1 = Depa.objects.filter(name=obj.cleaned_data['name']).values('useinfo__account')
    if ret1[0]['useinfo__account'] != None:
        for i in ret1:
            with open('%s%s' % (CCD_PATH, i['useinfo__account']), 'r') as u:
                lines = u.readlines()

            with open('%s%s' % (CCD_PATH, i['useinfo__account']), 'w') as f:
                for i in lines:
                    datas = i.strip()
                    if len(datas) != 0:
                        if 'route' in i:
                            continue
                        f.write(i + '\n')
                f.write('\n' + ret['routemgr__tactful'] + '\n')
    else:
        print("is empty")












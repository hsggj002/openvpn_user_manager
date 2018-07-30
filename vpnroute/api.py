# -*- coding:utf-8 -*-


from django import forms
from django.forms import fields
from django.forms import widgets

class RouteForm(forms.Form):
    name = fields.CharField(
        required=True,
        error_messages={'required': '路由名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','style':'width: 60%;'})
    )

    tactful = fields.CharField(
        required=False,
        widget=widgets.Textarea(attrs={'class':'form-control','style':'width: 60%;'})
        # widgets.TextInput
    )
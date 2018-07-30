#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import os, sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','openvpn.settings')
django.setup()
from vpn.models import *
from vpn.api import LoggerHelper
import logging
logger = LoggerHelper.instance()


def chkpwd(user,pwd):
    user = UseInfo.objects.get(account=user)
    if pwd == user.password:
        logger.run_logger.log(logging.INFO,'Successful authentication: username=%s' %user)
        sys.exit(0)
    else:
        logger.error_logger.log(logging.ERROR,'Incorrect username OR password: username=%s, password=%s' %(user,pwd))
        sys.exit(1)


if __name__ == "__main__":
    user = os.environ['username']
    pwd = os.environ['password']
    chkpwd(user,pwd)

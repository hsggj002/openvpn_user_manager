#-*- coding:utf-8 -*-
#Author: Guangjie Guo

import hashlib

def encrypt(pwd):
    obj = hashlib.md5()

    obj.update(pwd.encode('utf-8'))
    data = obj.hexdigest()
    return data
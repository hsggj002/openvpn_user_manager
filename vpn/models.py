from django.db import models

# Create your models here.

class UseInfo(models.Model):
    account = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32)

    address = models.OneToOneField('Netaddress',blank=True,null=True,on_delete=models.SET_NULL)
    depaer = models.ForeignKey("Depa",default=1,blank=True,null=True,on_delete=models.SET_NULL)

class Netaddress(models.Model):
    addrname = models.CharField(max_length=16)
    gw_addrname = models.CharField(max_length=16)
    flag = models.BooleanField(default=0)

    def __str__(self):
        return self.addrname

class Depa(models.Model):
    name = models.CharField(max_length=16)
    comment = models.CharField(max_length=16, blank=True, null=True)

    routemgr = models.ForeignKey('Routemgr',blank=True,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Routemgr(models.Model):
    name = models.CharField(max_length=16)
    tactful = models.TextField()

    def __str__(self):
        return self.name
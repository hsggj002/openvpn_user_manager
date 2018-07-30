"""openvpn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from vpn import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^initdb/', views.initdb),
    url(r'^index/$', views.index,name='index'),
    url(r'^$', views.acc_login),
    url(r'^login/$', views.acc_login),
    url(r'^user_list/$', views.user_list,name='user_list'),
    # url(r'^user_mgr/$', views.user_mgr,name='user_mgr'),
    url(r'^add_batch/$', views.add_batch,name='add_batch'),
    url(r'^add/$', views.add,name='add'),
    url(r'^logout/$', views.logout,name='logout'),
    url(r'^delete-id=(\d+)$', views.delete,name='delete'),
    url(r'^del-all', views.delete_all),
    url(r'^edit-id=(\d+)$', views.edit,name='edit'),
    url(r'^write_out/', views.write_out,name='write_out'),
    url(r'^vpngroup/', include('vpngroup.urls')),
    url(r'^vpnroute/', include('vpnroute.urls')),
    url(r'^vpnnetwork/', include('vpnnetwork.urls')),
    # url(r'^rule/$', views.rule, name='rule'),
    # url(r'^add_rule/$', views.add_rule, name='add_rule'),
    # url(r'^route/',include('route.urls')),
]

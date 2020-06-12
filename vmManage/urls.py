# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from . import vm
from vmManage import vip_manage
from vmManage import config_sync

urlpatterns = (
    url(r'^$', views.home),
    url(r'^dev-guide/$', views.dev_guide),
    url(r'^contact/$', views.contact),
    url(r'^hello/$', views.hello),
    url(r'^vm-list/$', vm.vms),
    url(r'^api-vms/$', vm.get_vms),
    url(r'^home/$', views.home),
    url(r'^vm/create/$', vm.create_vm_api),
    url(r'^vm-create/$', vm.create_vm),
    url(r'^vip-list/$', vip_manage.Vip.as_view(), name="get_vip"),
    url(r'^pool/$', vip_manage.Pool.as_view(), name="pool"),
    url(r'^config-sync/pool/$', config_sync.pool_sync),
    url(r'^config-sync/vs/$', config_sync.vs_sync),
    url(r'^auto/slb/locate/$', vip_manage.locate_slb),
)

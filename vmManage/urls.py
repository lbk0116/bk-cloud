# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from . import vm


urlpatterns = (
    url(r'^$', views.home),
    url(r'^dev-guide/$', views.dev_guide),
    url(r'^contact/$', views.contact),
    url(r'^hello/$', views.hello),
    url(r'^vm-list/$', vm.vms),
    url(r'^api-vms$', vm.get_vms),
    url(r'^home/$', views.home),
    url(r'^vm/create/$', vm.create_vm_api),
    url(r'^vm-create/$', vm.create_vm),
)

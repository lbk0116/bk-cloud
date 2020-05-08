# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from vmware.vapi.vsphere.client import create_vsphere_client
import requests
import urllib3


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render(request, 'home_application/dev_guide.html')


def contact(request):
    """
    联系页
    """
    return render(request, 'home_application/contact.html')

def hello(request):
    return HttpResponse("Hello lbk!")

def get_vm_list(request):
    session = requests.session()
    session.verify = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    vsphere_client = create_vsphere_client(server='10.12.0.3', username='libaokun@lab.ntjc', password='p@ssw0rd', session=session)

    vm_lists = vsphere_client.vcenter.VM.list()
    save_vm(vm_lists)
    return HttpResponse(vm_lists)


def save_vm(list):
    if list:
        for i in list:
            models.vm.objects.create(
                vm = i.vm,
                name = i.name,
                power_state = i.power_state,
                cpu_count = i.cpu_count,
                memory_size_mib = i.memory_size_mib
            )

# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.vcenter_client import VM
from com.vmware.vcenter.vm.hardware_client import Memory, Disk
# from . import models
# from .samples.vsphere.vcenter.helper import vm_placement_helper
import requests
import urllib3
import json

from com.vmware.vcenter_client import Datastore
from com.vmware.vcenter_client import Datacenter
from com.vmware.vcenter_client import Folder
from com.vmware.vcenter_client import ResourcePool


session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
vsphere_client = create_vsphere_client(server='10.12.0.3', username='libaokun@lab.ntjc', password='p@ssw0rd', session=session)

def get_vm_list(request):

    vm_lists = vsphere_client.vcenter.VM.list()
    # save_vm(vm_lists)

    return HttpResponse(vm_lists)

def get_vms(request):
    vm_list_oject = vsphere_client.vcenter.VM.list()
    for i in vm_list_oject:
        vm_list_str = []
        vm_list_str.append(i.__dict__)

    response_api = {
        "catalogues": {
            "vm": "虚机编号",
            "name": "虚机名称",
            "power_state": "电源",
            "cpu_count": "CPU",
            "memory_size_mib": "内存(M)"
        },
        "items": vm_list_str
    }
    # print(response_api)
    return JsonResponse(response_api)

def vms(request):

    return render(request, 'vm.html')

def save_vm(**kwargs):
    if kwargs:
        for i in kwargs:
            models.vm.objects.create(
                vm=i.vm,
                name=i.name,
                power_state=i.power_state,
                cpu_count=i.cpu_count,
                memory_size_mib=i.memory_size_mib
            )

def create_vm(request):
    return render(request, 'vm_create.html')

# 权限不足，调式不通过
# REST api接口
def create_vm_api(request):
    datacenter_name = 'BlueKing'
    vm_folder_name = 'test'
    datastore_name = 'esxi-1-hdd'
    # session = get_unverified_session()

    session = requests.session()
    session.verify = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = create_vsphere_client(server='10.12.33.9',
                                   username='administrator@lbk.vc',
                                   password='P@ssw0rd',
                                   session=session)

    # client = create_vsphere_client(server='10.12.0.3',
    #                                username=r'libaokun@lab.ntjc',
    #                                password=r'p@ssw0rd',
    #                                session=session)

    placement_spec = get_placement_spec_for_resource_pool(
        client,
        datacenter_name,
        vm_folder_name,
        datastore_name)

    rec_data = json.loads(request.body.decode('utf-8'), strict=False)
    guest_os = "WINDOWS_9"
    vm_name = rec_data['name']
    memory = Memory.UpdateSpec(size_mib=int(rec_data['memory']) * 1024)
    disk = Disk.CreateSpec(new_vmdk=Disk.VmdkCreateSpec(capacity=int(rec_data['disk']) * 1024 * 1024 * 1024))
    vm_create_spec = VM.CreateSpec(name=vm_name,
                                   guest_os=guest_os,
                                   memory=memory,
                                   disks=[disk],
                                   placement=placement_spec)

    vm = client.vcenter.VM.create(vm_create_spec)
    print("create_default_vm: Created VM '{}' ({})".format(vm_name, vm))

    vm_info = client.vcenter.VM.get(vm)

    if (vm_info):
        return JsonResponse({'code': 200, 'data': "create_default_vm: Created VM '{}' ({})".format(vm_name, vm)})
    else:
        return JsonResponse({'code': 500, 'message': "error"})

def get_placement_spec_for_resource_pool(client,
                                         datacenter_name,
                                         vm_folder_name,
                                         datastore_name):
    """
    Returns a VM placement spec for a resourcepool. Ensures that the
    vm folder and datastore are all in the same datacenter which is specified.
    """
    resource_pool = get_resource_pool(client,
                                      datacenter_name)

    folder = get_folder(client,
                        datacenter_name,
                        vm_folder_name)

    datastore = get_datastore(client,
                              datacenter_name,
                              datastore_name)

    # Create the vm placement spec with the datastore, resource pool and vm
    # folder
    placement_spec = VM.PlacementSpec(folder=folder,
                                      resource_pool=resource_pool,
                                      datastore=datastore)

    print("get_placement_spec_for_resource_pool: Result is '{}'".format(placement_spec))
    return placement_spec

def get_datastore(client, datacenter_name, datastore_name):
    """
    Returns the identifier of a datastore
    Note: The method assumes that there is only one datastore and datacenter
    with the mentioned names.
    """
    datacenter = get_datacenter(client, datacenter_name)
    if not datacenter:
        print("Datacenter '{}' not found".format(datacenter_name))
        return None

    filter_spec = Datastore.FilterSpec(names=set([datastore_name]),
                                       datacenters=set([datacenter]))

    datastore_summaries = client.vcenter.Datastore.list(filter_spec)
    if len(datastore_summaries) > 0:
        datastore = datastore_summaries[0].datastore
        return datastore
    else:
        return None

def get_datacenter(client, datacenter_name):
    """
    Returns the identifier of a datacenter
    Note: The method assumes only one datacenter with the mentioned name.
    """

    filter_spec = Datacenter.FilterSpec(names=set([datacenter_name]))

    datacenter_summaries = client.vcenter.Datacenter.list(filter_spec)
    if len(datacenter_summaries) > 0:
        datacenter = datacenter_summaries[0].datacenter
        return datacenter
    else:
        return None

def get_folder(client, datacenter_name, folder_name):
    """
    Returns the identifier of a folder
    Note: The method assumes that there is only one folder and datacenter
    with the mentioned names.
    """
    datacenter = get_datacenter(client, datacenter_name)
    if not datacenter:
        print("Datacenter '{}' not found".format(datacenter_name))
        return None

    filter_spec = Folder.FilterSpec(type=Folder.Type.VIRTUAL_MACHINE,
                                    names=set([folder_name]),
                                    datacenters=set([datacenter]))

    folder_summaries = client.vcenter.Folder.list(filter_spec)
    if len(folder_summaries) > 0:
        folder = folder_summaries[0].folder
        print("Detected folder '{}' as {}".format(folder_name, folder))
        return folder
    else:
        print("Folder '{}' not found".format(folder_name))
        return None

def get_resource_pool(client, datacenter_name, resource_pool_name=None):
    """
    Returns the identifier of the resource pool with the given name or the
    first resource pool in the datacenter if the name is not provided.
    """
    datacenter = get_datacenter(client, datacenter_name)
    if not datacenter:
        print("Datacenter '{}' not found".format(datacenter_name))
        return None

    names = set([resource_pool_name]) if resource_pool_name else None
    filter_spec = ResourcePool.FilterSpec(datacenters=set([datacenter]),
                                          names=names)

    resource_pool_summaries = client.vcenter.ResourcePool.list(filter_spec)
    if len(resource_pool_summaries) > 0:
        resource_pool = resource_pool_summaries[0].resource_pool
        print("Selecting ResourcePool '{}'".format(resource_pool))
        return resource_pool
    else:
        print("ResourcePool not found in Datacenter '{}'".
              format(datacenter_name))
        return None

if __name__ == '__main__':
    create_vm()
    # get_vms()

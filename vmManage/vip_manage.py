# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
import json
import requests
from vmManage import models


class Vip(View):
    """
        实现服务器负载vip类的实例化操作，对相关数据表的增删改查
        
    """
    def get(self, request):
        vip_objects = models.Vip.objects.all()
        vip_list = []
        for item in vip_objects:
            vip_dic = {}
            vip_dic['vip'] = item.vip
            vip_dic['vport'] = item.vport
            vip_dic['pool'] = item.pool.name
            vip_dic['device'] = item.device.name
            vip_dic['create_by_order_id'] = item.create_by_order_id
            # vip_dic['update_by_order_id'] = item.update_by_order_id
            # vip_dic['delete_by_order_id'] = item.delete_by_order_id
            vip_list.append(vip_dic)
        result = {"data": vip_list}
        return JsonResponse(result)

class Pool(View):
    """
        实现服务器负载均衡pool的增删改查操作
    """

    def get(self, request):
        vip_objects = models.Pool.objects.all()
        vip_list = []
        for item in vip_objects:
            vip_dic = {}
            vip_dic['name'] = item.name
            vip_dic['device'] = item.device_id.name

            vip_list.append(vip_dic)
        result = {"data": vip_list}
        return JsonResponse(result)

    def pool_create_params(self, name, partition, description='pool', *members):
        data = {}
        data['name'] = name
        data['description'] = description
        data['partition'] = partition
        # data['health_monitor'] = args.get('source', '/Common/ac_tcp')
        data['members'] = members
        print(data)
        return data    

    def post(self,request):

        big_ip = '10.12.32.1'
        user = 'admin'
        passwd = 'jcfwNT2018'
        partition = 'Common'
        health_monitor = '/Common/ac_tcp'

        request_data_json = json.loads(request.body.decode())
        pool_name = request_data_json['name']
        description = request_data_json['description']
        members = request_data_json['members']
        # members = [{"name": "member_test_21:500", "address": "10.12.248.54"},{"name": "member_test_22:344", "address": "10.12.248.45"}]
        # requests.packages.urllib3.disable_warnings()

        b = requests.session()
        b.auth = (user, passwd)
        b.verify = False
        b.headers.update({'Content-Type': 'application/json'})

        post_data = self.pool_create_params(pool_name, partition, description, *members)

        try:
            print("join to post config in f5")
            # 接口请求体数据格式
            # {
            #     "name": "lbk101",
            #     "description": "libaokun test",
            #     "members": [{"name": "member_test_21:500", "address": "10.12.248.54"},{"name": "member_test_22:344", "address": "10.12.248.45"}]
            # }
            ret = b.post('https://{}/mgmt/tm/{}'.format(big_ip, 'ltm/pool'),
                data=json.dumps(post_data, ensure_ascii=False).encode('utf-8'))
            print(ret.text)
        except Exception as e:
            print(e)
        
        return JsonResponse({'status': ret.status_code})
 

def locate_slb(request):
    """
        根据需求自动定位待变更的负载均衡设备
        定位设备算法如下：
        1、根据服务器区域查找该区域下对应的负载均衡；
        2、
    """
    slb_device = models.Device.objects.all()[0]
    return JsonResponse({"device_ip": slb_device.mgt_ip})

def is_conflict(request):
    """
        查询设备实时配置，判断需求是否跟当前配置冲突
        有冲突，返回1
        无冲突，返回0
    """
    return JsonResponse({"result": 0})
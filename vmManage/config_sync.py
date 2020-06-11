# -*- coding: utf-8 -*-
import requests
from vmManage import models
import json
from django.http import JsonResponse
import sys


user = 'admin'
passwd = 'jcfwNT2018'
partition = 'Common'
health_monitor = '/Common/ac_tcp'


def pool_sync(request):
    request_data_json = json.loads(request.body.decode())
    big_ip = request_data_json['mgt_ip']
    device_object = models.Device.objects.get(mgt_ip=big_ip)

    req = requests.Session()
    req.auth = (user, passwd)
    req.verify = False
    req.headers.update({'Content-Type': 'application/json'})

    url = "https://{}/mgmt/tm/{}".format(big_ip, 'ltm/pool')
    # 发起请求查询pool信息
    # F5查询pool返回消息体
    """
    {
    "kind": "tm:ltm:pool:poolcollectionstate",
    "selfLink": "https://localhost/mgmt/tm/ltm/pool?ver=14.0.0.3",
    "items": [
        {
            "kind": "tm:ltm:pool:poolstate",
            "name": "lbk101",
            "partition": "Common",
            "fullPath": "/Common/lbk101",
            "generation": 428,
            "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~lbk101?ver=14.0.0.3",
            "allowNat": "yes",
            "allowSnat": "yes",
            "description": "libaokun test",
            "ignorePersistedWeight": "disabled",
            "ipTosToClient": "pass-through",
            "ipTosToServer": "pass-through",
            "linkQosToClient": "pass-through",
            "linkQosToServer": "pass-through",
            "loadBalancingMode": "round-robin",
            "minActiveMembers": 0,
            "minUpMembers": 0,
            "minUpMembersAction": "failover",
            "minUpMembersChecking": "disabled",
            "queueDepthLimit": 0,
            "queueOnConnectionLimit": "disabled",
            "queueTimeLimit": 0,
            "reselectTries": 0,
            "serviceDownAction": "none",
            "slowRampTime": 10,
            "membersReference": {
                "link": "https://localhost/mgmt/tm/ltm/pool/~Common~lbk101/members?ver=14.0.0.3",
                "isSubcollection": true
            }
        }
    ]
    }
    """

    res_pool = req.get(url)
    res_pool_json = json.loads(res_pool.content)
    for itsm in res_pool_json['items']:
        pool_name = itsm['name']
        # description = itsm['description']
        # members引用对象，包括url
        membersReference = itsm['membersReference']['link']
        url_member = membersReference.replace('localhost',big_ip)
        # 发起请求查询members信息
        # F5查询member返回消息体
        """
        {
            "kind": "tm:ltm:pool:members:memberscollectionstate",
            "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~lbk101/members?ver=14.0.0.3",
            "items": [
                {
                "kind": "tm:ltm:pool:members:membersstate",
                "name": "member_test_21:500",
                "partition": "Common",
                "fullPath": "/Common/member_test_21:500",
                "generation": 428,
                "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~lbk101/members/~Common~member_test_21:500?ver=14.0.0.3",
                "address": "10.12.248.54",
                "connectionLimit": 0,
                "dynamicRatio": 1,
                "ephemeral": "false",
                "fqdn": {
                    "autopopulate": "disabled"
                },
                "inheritProfile": "enabled",
                "logging": "disabled",
                "monitor": "default",
                "priorityGroup": 0,
                "rateLimit": "disabled",
                "ratio": 1,
                "session": "user-enabled",
                "state": "unchecked"
                }
            ]
        }
        """
        res_member = req.get(url_member)
        res_member_json = json.loads(res_member.content)

        # 入库
        try:
            pool_object = models.Pool.objects.create(name=pool_name,device=device_object)

            for member in res_member_json['items']:
                member_name = member['name']
                member_port = member_name.split(':')[1]
                ip = member['address']

                try:
                    models.Members.objects.create(name=member_name, ip=ip, port=member_port, pool=pool_object, device=device_object)
                except Exception as e:
                    print(e)
                finally:
                    pass

        except Exception as e:
            if "Duplicate entry" in e.__str__():
                # info = sys.exc_info()
                # print( info[0], ":", info[1])
                print(e.__str__())
                continue

    return JsonResponse({"status": 200})

def vs_sync(request):
    # 发起请求查询vs信息
    # F5查询vs返回消息体
    """
    {
        "kind": "tm:ltm:virtual:virtualcollectionstate",
        "selfLink": "https://localhost/mgmt/tm/ltm/virtual?ver=14.0.0.3",
        "items": [
            {
            "kind": "tm:ltm:virtual:virtualstate",
            "name": "final_profile",
            "partition": "Common",
            "fullPath": "/Common/final_profile",
            "generation": 1,
            "selfLink": "https://localhost/mgmt/tm/ltm/virtual/~Common~final_profile?ver=14.0.0.3",
            "addressStatus": "yes",
            "autoLasthop": "default",
            "cmpEnabled": "yes",
            "connectionLimit": 0,
            "creationTime": "2019-03-06T12:44:24Z",
            "description": "哈哈哈",
            "destination": "/Common/10.12.248.34:443",
            "enabled": true,
            "gtmScore": 0,
            "ipProtocol": "tcp",
            "lastModifiedTime": "2019-03-05T13:20:19Z",
            "mask": "255.255.255.255",
            "mirror": "disabled",
            "mobileAppTunnel": "disabled",
            "nat64": "disabled",
            "pool": "/Common/test_pool",
            "poolReference": {
                "link": "https://localhost/mgmt/tm/ltm/pool/~Common~test_pool?ver=14.0.0.3"
            },
            "rateLimit": "disabled",
            "rateLimitDstMask": 0,
            "rateLimitMode": "object",
            "rateLimitSrcMask": 0,
            "serviceDownImmediateAction": "none",
            "source": "0.0.0.0/0",
            "sourceAddressTranslation": {
                "pool": "/Common/snat-pool-whp",
                "poolReference": {
                "link": "https://localhost/mgmt/tm/ltm/snatpool/~Common~snat-pool-whp?ver=14.0.0.3"
                },
                "type": "snat"
            },
            "sourcePort": "preserve",
            "synCookieStatus": "not-activated",
            "translateAddress": "enabled",
            "translatePort": "enabled",
            "vlansDisabled": true,
            "vsIndex": 3,
            "persist": [
                {
                "name": "test_addr_000001",
                "partition": "Common",
                "tmDefault": "yes",
                "nameReference": {
                    "link": "https://localhost/mgmt/tm/ltm/persistence/source-addr/~Common~test_addr_000001?ver=14.0.0.3"
                }
                }
            ],
            "policiesReference": {
                "link": "https://localhost/mgmt/tm/ltm/virtual/~Common~final_profile/policies?ver=14.0.0.3",
                "isSubcollection": true
            },
            "profilesReference": {
                "link": "https://localhost/mgmt/tm/ltm/virtual/~Common~final_profile/profiles?ver=14.0.0.3",
                "isSubcollection": true
            }
            }
        ]
    }
    """
    request_data_json = json.loads(request.body.decode())
    big_ip = request_data_json['mgt_ip']
    device_object = models.Device.objects.get(mgt_ip=big_ip)

    req = requests.Session()
    req.auth = (user, passwd)
    req.verify = False
    req.headers.update({'Content-Type': 'application/json'})

    url_vs = "https://{}/mgmt/tm/{}".format(big_ip, 'ltm/virtual')
    res_vs = req.get(url_vs)
    res_vs_json = json.loads(res_vs.content)
    vs_list = res_vs_json['items']
    for item in vs_list:
        destination = item['destination']
        vip = destination.split('/')[2].split(':')[0]
        vport = destination.split('/')[2].split(':')[1]
        device_object = models.Device.objects.get(mgt_ip=big_ip)
        pool_name = item['poolReference']['link'].split('~')[2].split('?')[0]
        pool_object = models.Pool.objects.get(name=pool_name)
        
        try:
            models.Vip.objects.create(vip=vip, vport=vport, device=device_object, pool=pool_object)
        except Exception as e:
            print(e)
        finally:
            pass

    return JsonResponse({"status": 200})

        
#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import os
import sys

def _now(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)

##### 可在脚本开始运行时调用，打印当时的时间戳及PID。
def job_start():
    print "[%s][PID:%s] job_start" % (_now(), os.getpid())

##### 可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。 
def job_success(msg):
    print "[%s][PID:%s] job_success:[%s]" % (_now(), os.getpid(), msg)
    sys.exit(0)

##### 可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
def job_fail(msg):
    print "[%s][PID:%s] job_fail:[%s]" % (_now(), os.getpid(), msg)
    sys.exit(1)
    
import requests, json
requests.packages.urllib3.disable_warnings()
import argparse
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--big_ip', type=str, required=True, default = None)
parser.add_argument('--f5-user', type=str, required=True, default='admin')
parser.add_argument('--f5-passwd', type=str, required=True, default='jcfwNT2018')
parser.add_argument('--pool_name', type=str, required=True, default='pool-100')
parser.add_argument('--description', type=str, default='')
parser.add_argument('--partition', type=str, default='Common')
parser.add_argument('--health_monitor', type=str, default='/Common/ac_tcp')
parser.add_argument('--members', type=str, required=True)
args = parser.parse_args()

big_ip = args.big_ip
user = args.f5_user
passwd = args.f5_passwd

b = requests.session()
b.auth = (user, passwd)
b.verify = False
b.headers.update({'Content-Type': 'application/json'})


def pool_create():
    data = {}
    data['name'] = args.pool_name
    data['description'] = args.description
    data['partition'] = args.partition
    # data['health_monitor'] = args.get('source', '/Common/ac_tcp')
    data['members'] = json.loads(args.members)
    return data    

if __name__ == '__main__':

    job_start()

###### 可在此处开始编写您的脚本逻辑代码
###### iJobs中执行脚本成功和失败的标准只取决于脚本最后一条执行语句的返回值
###### 如果返回值为0，则认为此脚本执行成功，如果非0，则认为脚本执行失败
    try:
        ret = b.post('https://{}/mgmt/tm/{}'.format(big_ip, 'ltm/pool'),
             data=json.dumps(pool_create(), ensure_ascii=False).encode('utf-8'))
        print(ret.text)
    except Exception as e:
        print(e)
        job_fail('error')
    if ret:
        print(ret.text)
        job_success('ok')

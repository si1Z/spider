#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 10:51
# @Author  : zhujinghui
# @File    : min_redis_init.py
# @Software: PyCharm

import redis
import time
import json
from datetime import datetime,timedelta

def get_Dynamic_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_400 = client.smembers("symbols400")
    codeset_temp = client.smembers("symbols.temp")
    codeset = codeset_400 | codeset_temp
    return codeset

def onlySetUrlList():
    # client = redis.Redis(host='10.11.9.7', port=6379, db=15, password='centos_data_123456', decode_responses=True)
    client = redis.Redis(host='10.11.9.12', port=6379, db=0, password='foobared', decode_responses=True)
    if client.exists('xueqiu_min_redis:start_urls'):
        return

    codeset = {'SP500', 'DJI30'}

    # codeset = get_Dynamic_Symbols()

    for code in codeset:
        url = "https://xueqiu.com/stock/forchart/stocklist.json?symbol={}&period=1d&one_min=1".format(code)
        client.rpush('xueqiu_min_redis:start_urls', url)

def onlyEmptyTaskList():
    # client = redis.Redis(host='10.11.9.7', port=6379, db=0, password='centos_data_123456', decode_responses=True)
    client = redis.Redis(host='10.11.9.12', port=6379, db=0, password='foobared', decode_responses=True)
    if not client.exists('xueqiu_min_redis:start_urls'):
        return
    for i in range(100):
        client.delete('xueqiu_min_redis:start_urls')
        time.sleep(.5)

def minRedisBak():
    #r = redis.Redis(host='59.110.24.235', password='root_db', port=6379, db=6)
    r = redis.Redis(host='47.94.19.25', password='root_db', port=6379, db=6)
    flag = False
    today = json.loads(r.hget('min0', 'AAPL').decode().replace("'", '"'))
    try:
        yesterday = json.loads(r.hget('min1', 'AAPL').decode().replace("'", '"'))
        if not (today[0]['time'] == yesterday[0]['time']):
            flag = True
    except:
        flag = True

    if flag:
        for i in range(4, 0, -1):
            try:
                r.rename('min' + str(i - 1), 'min' + str(i))
            except:
                print('.............')

startbaktime = datetime.strptime("10:29:10","%H:%M:%S").time()
begintime = datetime.strptime("10:29:50","%H:%M:%S").time()
endtime = datetime.strptime("17:10:00","%H:%M:%S").time()

# while True:
#     now = datetime.now()
#     #转换成美国时间
#     us_now = now - timedelta(hours=12)
#
#     if us_now.isoweekday() in (1,2,3,4,5):
#         usnowtime = us_now.time()
#         try:
#             #if startbaktime < usnowtime < begintime:
#             #    minRedisBak()
#             if  begintime < usnowtime < endtime:
#                 onlySetUrlList()
#             if usnowtime > endtime or usnowtime < begintime:
#                 onlyEmptyTaskList()
#             print('美国时间:'+ str(us_now),end='\r')
#             time.sleep(3)
#         except:
#             time.sleep(5)
#     else:
#         print('美国时间:' + str(us_now), end='\r')
#         time.sleep(3)

# onlySetUrlList()
# onlyEmptyTaskList()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 9:37
# @Author  : zhujinghui
# @File    : xueqiu_redis_controller.py
# @Software: PyCharm
import time
import redis
import pymysql
from datetime import datetime,timedelta

def get_Dynamic_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_400 = client.smembers("symbols400")
    codeset_temp = client.smembers("symbols.temp")
    codeset = codeset_400 | codeset_temp
    return codeset

def get_Code_List_List(codes,n=50):
    list_list = []
    code_list = list(codes)
    for i in range(0, len(code_list), n):
        list_list.append(code_list[i:i + n])
    return list_list

def onlySetUrlList(n = 5):
    codeset = get_Dynamic_Symbols()

    client = redis.Redis(host='10.11.9.12', port=6379, db=0, password='foobared', decode_responses=True)
    if client.exists('xueqiu_redis:start_urls'):
        return

    code_list_list = get_Code_List_List(codeset)
    for i in range(n):
        for code50 in code_list_list:
            url = "https://xueqiu.com/v4/stock/quote.json?code=" + ",".join(code50)
            client.rpush('xueqiu_redis:start_urls', url)

def onlyEmptyTaskList():
    client = redis.Redis(host='10.11.9.12', port=6379, db=0, password='foobared', decode_responses=True)
    if not client.exists('xueqiu_redis:start_urls'):
        return
    for i in range(100):
        client.delete('xueqiu_redis:start_urls')
        time.sleep(.5)

def truncatetable(table="stock_kuaizhao"):
    # conn = pymysql.connect(host="10.9.210.109", user="liangxiang", passwd="lx_2017_xhyg", db="ra_online", port=3306,charset='utf8')
    conn = pymysql.connect(host="rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com", user="yigukeji_db",
                           passwd="Yigukeji_dba", db="xhyg_us_stocks", port=3306, charset='utf8')
    cursor = conn.cursor()
    sql = "truncate table " + table
    cursor.execute(sql)
    conn.commit()
    conn.close()

truncatetime = datetime.strptime("9:28:10","%H:%M:%S").time()
begintime = datetime.strptime("9:29:50","%H:%M:%S").time()
endtime = datetime.strptime("21:30:00","%H:%M:%S").time()
#
# while True:
#     now = datetime.now()
#     #转换成美国时间
#     us_now = now - timedelta(hours=12)
#     if us_now.isoweekday() in (1,2,3,4,5):
#         usnowtime = us_now.time()
#         try:
#             if truncatetime < usnowtime < begintime:
#                 truncatetable()
#             if  begintime < usnowtime < endtime:
#                 onlySetUrlList()
#             if usnowtime > endtime or usnowtime < begintime:
#                 onlyEmptyTaskList()
#             print('美国时间:'+ str(us_now),end='\r')
#             time.sleep(3)
#         except Exception as e:
#             print(e)
#             time.sleep(5)
#     else:
#         print('美国时间:' + str(us_now), end='\r')
#         time.sleep(3)

# onlySetUrlList()
onlyEmptyTaskList()

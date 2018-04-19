#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 18:35
# @Author  : zhujinghui
# @File    : min0.py
# @Software: PyCharm
import redis
def get_All_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_8000 = client.smembers("symbols8000")
    return list(codeset_8000)

def get_Dynamic_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_400 = client.smembers("symbols400")
    codeset_temp = client.smembers("symbols.temp")
    codeset = codeset_400 | codeset_temp
    # codeset = codeset_temp
    return list(codeset)

symbols = get_All_Symbols()
if "LX" in symbols:
    print("xxxxxxxx")
#
# def set_All_Symbols():
#     client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
#     client.sadd("symbols8000","SOGO")
#     # codeset_8000 = client.smembers("symbols8000")
#     # return list(codeset_8000)
# # set_All_Symbols()
# symbols = get_All_Symbols()
# if "SOGO" in symbols:
#     print("xxxxxxxx")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 16:17
# @Author  : zhujinghui
# @File    : code_tools.py
# @Software: PyCharm
import redis

def get_Dynamic_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_400 = client.smembers("symbols400")
    codeset_temp = client.smembers("symbols.temp")
    codeset = codeset_400 | codeset_temp
    return list(codeset)

def get_All_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_8000 = client.smembers("symbols8000")
    return list(codeset_8000)

# 分组
def get_Code_List_List(codes,n=50):
    list_list = []
    code_list = list(codes)
    for i in range(0, len(code_list), n):
        list_list.append(code_list[i:i + n])
    return list_list
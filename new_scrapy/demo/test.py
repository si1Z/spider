#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 14:15
# @Author  : zhujinghui
# @File    : test.py
# @Software: PyCharm
import requests
import json

def get_news_lasttime(code):
    url = "https://www.xinbozhengquan.com/bussiness/news_service/query_news_last.json"
    # url = "http://39.106.143.83:8070/bussiness/news_service/query_news_last.json"
    data_dict = {"tagStock":[code]}

    datajsonstr = json.JSONEncoder().encode(data_dict)
    rsp= requests.post(url, datajsonstr)
    resultjson=json.JSONDecoder().decode(rsp.text)
    try:
        newstime = resultjson['data']['sourcetime']
        return newstime
    except:
        return ''

print(get_news_lasttime('AAPL'))
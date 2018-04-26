#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 下午7:23
# @Author  : zhujinghui 
# @site    : 
# @File    : 1.py
# @Software: PyCharm

import requests

url = "https://api.finbtc.net/app/market/coin/toplist"


headers = {
    'X-App':'1.6.0/inviting20180419/android',
    'device':'a1c27505-c7a7-41c1-92e8-cd308756cc5',
    'User-Agent':'okhttp/3.9.1'
}

rsp = requests.get(url,headers=headers,verify=False)

print(rsp.text)
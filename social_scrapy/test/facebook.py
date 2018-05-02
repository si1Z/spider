#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 下午3:27
# @Author  : zhujinghui 
# @site    : 
# @File    : facebook.py
# @Software: PyCharm
import requests
from scrapy.http import HtmlResponse

# url = "https://www.facebook.com/ethereumproject"
#
#
# text = requests.get(url).text
#
# with open('p.txt','w',encoding='utf-8') as f:
#     f.write(text)

with open('tmp.txt','r') as f:
    text = f.read()

response = HtmlResponse(url='http://www.test.com',body=text,encoding='utf-8')

div = response.xpath('//div[@class="_4-u2 _6590 _3xaf _4-u8"]')[0]

ds_9 = div.xpath(".//div[@class='_4bl9']")

tmp = ds_9[0].xpath('.//text()').extract_first()
print(tmp)
# for d in ds_9:
#     print(d)
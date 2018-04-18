#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 上午10:13
# @Author  : zhujinghui 
# @site    : 
# @File    : test.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup

# url = "https://nebulas.io/team.html"

def geturl():

    url = "https://info.binance.com/"

    proxies = { "https": "https://127.0.0.1:1087"}
    rsp = requests.get(url, proxies=proxies)

    text = rsp.text

    with open('tmp.txt','w',encoding='utf-8') as f:
        f.write(text)

    with open('tmp.txt','r',encoding='utf-8') as f:
        text = f.read()

    soup = BeautifulSoup(rsp.text,'lxml')
    body = soup.find('tbody')
    trs = body.find_all('tr',recursive=False)

    base_url = 'https://info.binance.com{}'
    for tr in trs:
        yield base_url.format(tr.get('link'))
        # print(tr.get('link'))


def get_describtion(url):

    proxies = {"https": "https://127.0.0.1:1087"}
    rsp = requests.get(url, proxies=proxies)


    text = rsp.text

    with open('tmp1.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    with open('tmp1.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'lxml')
    div = soup.find('div',class_='content-box')



    content_top = div.find('div',class_='row content-top')
    maket_info = content_top.find('div',class_='row maket-info')

    divs = maket_info.find_all('div',recursive=False)

    # for tmp in divs:
    #     print(tmp)


    content_text = div.find('div',class_='content-text')
    print(content_text.p.text)

#
# urls = geturl()
#
# for url in urls:
#     get_describtion(url)

url = "https://info.binance.com/cn/currencies/litecoin"
get_describtion(url)

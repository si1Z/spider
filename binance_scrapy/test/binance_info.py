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



    #上边
    content_top = div.find('div',class_='row content-top')
    #。。。。左边
    h4 = content_top.find('h4',class_='media-heading')
    symbol = h4.font.text
    name = h4.span.text.replace('(',"").replace(')',"")
    #。。。。右边
    maket_info=content_top.find('div',class_='row maket-info')
    divs = maket_info.find_all('div',recursive=False)

    for tmp in divs:

        if str(tmp.span.text).startswith('Market Cap'):
            pass
        if str(tmp.span.text).startswith('Max Supply'):
            pass
            # print(tmp.strong.text)
        if str(tmp.span.text).startswith('Circulating Supply'):
            pass
            print(tmp.strong.text)
        if str(tmp.span.text).startswith('Issue Price'):
            symb = tmp.find('strong',class_='symbol').text
            num = tmp.find('font',class_='symbolNum three').text
            issue_price = "{}{}".format(symb,num)

        if str(tmp.span.text).startswith('Issue Date'):
            issue_date = tmp.find('strong').text

    #左边
    ul_left = div.find('ul', class_='pull-left')
    lis_left = ul_left.find_all('li')
    for li_left in lis_left:
        if str(li_left.text).startswith("Website"):
            website = li_left.a.get('href')#................
        if str(li_left.text).startswith("Explorer"):
            explorer = li_left.a.get('href')#................
        if str(li_left.text).startswith("White Paper"):
            white_paper_en = li_left.a.get('href')#................

    # print(website)
    # print(explorer)
    # print(white_paper_en)

    #右边
    social = {}
    ul_right = div.find('ul', class_='pull-right')
    if ul_right != None:
        lis_right = ul_right.find_all('li')
        del lis_right[0]
        for li_right in lis_right:
            # print(li_right.a.get('title'))
            # print(li_right.a.get('href'))
            social[li_right.a.get('title')] = li_right.a.get('href')

    # print(social)

    #介绍
    content_text = div.find('div',class_='content-text')
    content_text_con = content_text.find('div',class_='content-text-con')
    ps = content_text_con.find_all('p')
    introduction_list = []
    for p in ps:
        introduction_list.append(p.text)
    introduction = '\n'.join(introduction_list)
    # print(introduction)  #.............................


#
# urls = geturl()
#
# for url in urls:
#     get_describtion(url)

url = "https://info.binance.com/en/currencies/neo"
# url = "https://info.binance.com/cn/currencies/neo"
get_describtion(url)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 8:52
# @Author  : zhujinghui
# @File    : test.py
# @Software: PyCharm
import requests
import json

# def get_news_lasttime(code):
#     url = "https://www.xinbozhengquan.com/bussiness/news_service/query_news_last.json"
#     data_dict = {"tagStock":[code]}
#
#     datajsonstr = json.JSONEncoder().encode(data_dict)
#     rsp= requests.post(url, datajsonstr)
#     resultjson=json.JSONDecoder().decode(rsp.text)
#     print(resultjson)
#     try:
#         newstime = resultjson['data']['sourcetime']
#         return newstime
#     except:
#         return ''
#
# tmp = get_news_lasttime('AAPL')
# print(tmp)

import scrapy
import ast
import re
from bs4 import BeautifulSoup

def err_log(description,url):
    with open('err.txt', 'a', encoding='utf-8') as f:
        f.write(description+":"+url+"\n")

# 解析非标准JSON的Javascript字符串
def parse_js(expr):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    m = ast.parse(expr)
    a = m.body[0]

    def parse(node):
        if isinstance(node, ast.Expr):
            return parse(node.value)
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Dict):
            return dict(zip(map(parse, node.keys), map(parse, node.values)))
        elif isinstance(node, ast.List):
            return map(parse, node.elts)
        else:
            raise NotImplementedError(node.__class__)

    return parse(a)

class NewsArticleItem(scrapy.Item):
    #股票号
    symbol = scrapy.Field()
    #时间
    newsdate = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 内容
    body = scrapy.Field()
    #关键字
    keywords = scrapy.Field()
    # 网址
    newsurl = scrapy.Field()
    # 来源
    source = scrapy.Field()


def parse_finance_page(response):
    parent = response.meta['parent']
    url = parent['newsurl']

    html = response.body.decode("gbk")
    soup = BeautifulSoup(html, 'lxml')

    item = NewsArticleItem()
    item['title'] = parent['simpletext']
    item['newsdate'] = parent['newsdate']
    item['symbol'] = parent['symbol']
    item['newsurl'] = parent['newsurl']

    try:
        tmpelement = soup.find('span', attrs={'bosszone': "jgname"})
        if tmpelement != None:
            item['source'] = tmpelement.text
        else:
            item['source'] = soup.find('span', class_='infoCol').find('span', class_='where').text
    except:
        item['source'] = "腾讯新闻"
        err_log("source",url)


    try:
        ps = soup.find('div', attrs={'id': "Cnt-Main-Article-QQ"}).find_all('p', recursive=False)
        text = str()
        for p in ps:
            ss = p.get_text()
            # 兼容有视频的情况
            if ss == '精彩视频推荐':
                break
            if ss != None and ss.strip() != '':
                text = text + str(ss).strip() + "\n"
        item['body'] = re.sub('^\n+', '', text)
    except:
        err_log("body", url)

    try:
        kere = re.compile("""ARTICLE_INFO = window.ARTICLE_INFO \|\|([\s\S]*?)</script>""")
        sst = kere.findall(html)[0].strip()
        item['keywords'] = parse_js(sst)['sosokeys']
    except:
        item['keywords'] = '{}'

    return item

#页面解析函数
def parse_tech_page(response):
    parent = response.meta['parent']
    url = parent['newsurl']

    html = response.body.decode("gbk")
    soup = BeautifulSoup(html, 'lxml')

    item = NewsArticleItem()
    item['title'] = parent['simpletext']
    item['newsdate'] = parent['newsdate']
    item['symbol'] = parent['symbol']
    item['newsurl'] = parent['newsurl']

    try:
        tmpelement = soup.find('span', attrs={'bosszone': "jgname"})
        if tmpelement != None:
            item['source'] = tmpelement.text
        else:
            item['source'] = soup.find('span', class_='infoCol').find('span', class_='where').text
    except:
        item['source'] = "腾讯新闻"
        err_log("source",url)

    try:
        ps = soup.find('div', attrs={'id': "Cnt-Main-Article-QQ"}).find_all('p', recursive=False)
        text = str()
        for p in ps:
            ss = p.get_text()
            # 兼容有视频的情况
            if ss == '精彩视频推荐':
                break

            if ss != None and ss.strip() != '':
                text = text + str(ss).strip() + "\n"
        item['body'] = re.sub('^\n+', '', text)
    except:
        err_log("body", url)

    try:
        kere = re.compile("""ARTICLE_INFO = window.ARTICLE_INFO \|\|([\s\S]*?)</script>""")
        sst = kere.findall(html)[0].strip()
        item['keywords'] = parse_js(sst)['sosokeys']
    except:
        item['keywords'] = '{}'

    return item

def parse1(html):
    soup = BeautifulSoup(html, 'lxml')
    item = NewsArticleItem()
    try:
        tmpelement = soup.find('span', attrs={'bosszone': "jgname"})
        if tmpelement != None:
            item['source'] = tmpelement.text
        else:
            item['source'] = soup.find('span', class_='infoCol').find('span', class_='where').text
    except:
        item['source'] = "腾讯新闻"
        err_log("source",url)


    try:
        ps = soup.find('div', attrs={'id': "Cnt-Main-Article-QQ"}).find_all('p', recursive=False)
        text = str()
        for p in ps:
            ss = p.get_text()
            # 兼容有视频的情况
            if ss == '精彩视频推荐':
                break
            if ss != None and ss.strip() != '':
                text = text + str(ss).strip() + "\n"
        item['body'] = re.sub('^\n+', '', text)
    except:
        err_log("body", url)

    try:
        kere = re.compile("""ARTICLE_INFO = window.ARTICLE_INFO \|\|([\s\S]*?)</script>""")
        sst = kere.findall(html)[0].strip()
        item['keywords'] = parse_js(sst)['sosokeys']
    except:
        item['keywords'] = '{}'

    return item

def parse2(html):
    soup = BeautifulSoup(html, 'lxml')
    item = NewsArticleItem()
    try:
        tmpelement = soup.find('span', attrs={'bosszone': "jgname"})
        if tmpelement != None:
            item['source'] = tmpelement.text
        else:
            item['source'] = soup.find('span', class_='infoCol').find('span', class_='where').text
    except:
        item['source'] = "腾讯新闻"
        err_log("source", url)

    # try:
    ps = soup.find('div', attrs={'id': "Cnt-Main-Article-QQ"}).find_all('p', recursive=False)
    text = str()
    for p in ps:
        ss = p.get_text()
        # 兼容有视频的情况
        if ss == '精彩视频推荐':
            break

        if ss.strip().startswith('var related_video_info ='):
            break
        if ss != None and ss.strip() != '':
            text = text + str(ss).strip() + "\n"
    item['body'] = re.sub('^\n+', '', text)
    # except:
    #     print(type(ss))
    #     err_log("body", url)

    try:
        kere = re.compile("""ARTICLE_INFO = window.ARTICLE_INFO \|\|([\s\S]*?)</script>""")
        sst = kere.findall(html)[0].strip()
        item['keywords'] = parse_js(sst)['sosokeys']
    except:
        item['keywords'] = '{}'

    return item


url = 'http://tech.qq.com/a/20160310/047765.htm'
rsp = requests.get(url)
html = rsp.text
item = parse2(html)
print(item)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 20:19
# @Author  : zhujinghui
# @File    : 2.py
# @Software: PyCharm
import ast
import scrapy
import re
import requests
from bs4 import BeautifulSoup

#解析非标准JSON的Javascript字符串
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
def err_log(description,url):
    pass
    # with open('err.txt', 'a', encoding='utf-8') as f:
    #     f.write(description+":"+url+"\n")

class NewsSimpleItem(scrapy.Item):
    #时间
    newsdate = scrapy.Field()
    # tmp
    tmp = scrapy.Field()
    # 内容摘录
    simpletext= scrapy.Field()
    # 网址
    newsurl = scrapy.Field()
    #股票号
    symbol = scrapy.Field()
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

#页面解析函数
def parse_tech_page(html):
    # parent = response.meta['parent']
    # url = parent['newsurl']

    # html = response.body.decode("gbk")
    soup = BeautifulSoup(html, 'lxml')

    item = NewsArticleItem()
    # item['title'] = parent['simpletext']
    # item['newsdate'] = parent['newsdate']
    # item['symbol'] = parent['symbol']
    # item['newsurl'] = parent['newsurl']

    try:
        tmpelement = soup.find('span', attrs={'bosszone': "jgname"})
        if tmpelement != None:
            item['source'] = tmpelement.text
        else:
            item['source'] = soup.find('span', class_='infoCol').find('span', class_='where').text
    except:
        item['source'] = "腾讯新闻"
        # err_log("source",url)

    try:
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
    except:
        # err_log("body", url)
        pass

    try:
        kere = re.compile("""ARTICLE_INFO = window.ARTICLE_INFO \|\|([\s\S]*?)</script>""")
        sst = kere.findall(html)[0].strip()
        item['keywords'] = parse_js(sst)['sosokeys']
    except:
        item['keywords'] = '{}'

    return item

url = "http://tech.qq.com/a/20180103/001463.htm"

rsp = requests.get(url)
html = rsp.text
data = parse_tech_page(html)
print(data)
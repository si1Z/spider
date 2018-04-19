# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsSimpleItem
from ..items import NewsArticleItem
from bs4 import BeautifulSoup
import random
import ast
import re
import redis
import requests
import json
import pickle
import sys

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
#解析url参数,返回字典
def urlparams(url):
    params = str(url).split('?')[-1].split('&')
    param_dict = {}
    for param in params:
        cols = param.split('=')
        param_dict[cols[0].strip()] = cols[1].strip()
    return param_dict

#获得redis里存有的股票代码列表
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

#生成起始url列表
def get_start_urls(codes=get_Dynamic_Symbols()):
    for code in codes:
        try:
            rediscache.set_redis(code,get_news_lasttime(code))
            baseurl = "http://news.gtimg.cn/more.php?q=us{}&page=1&_du_r_t={}".format(code, str(random.random())[:-2])
            yield baseurl
        except:
            continue

def err_log(description,url):
    with open('err.txt', 'a', encoding='utf-8') as f:
        f.write(description+":"+url+"\n")

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

def parse_stock_page(response):
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

def parse_news_page(response):
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

#......................................
#全量抓取的.......................
class TxNewsSpider(scrapy.Spider):
    name = "tx_news"
    start_urls = get_start_urls()
    custom_settings = {
        'MONGODB_SERVER':'10.11.9.7',
        'MONGODB_PORT':27017,
        'MONGODB_DB':'mongodb',
        'MONGODB_COLLECTION':'news',
        'ITEM_PIPELINES': {
            # 'new_scrapy.pipelines.ServiceArticlePipeline': 100,
            'new_scrapy.pipelines.MongoDBPipeline':100
        },
    }

    def parse(self, response):
        text = response.body.decode("gbk")
        jsontext = text.replace('var finance_news =','').replace("'",'"').strip()[:-1]
        jso_dict = json.loads(jsontext)

        total = jso_dict['total']
        current = jso_dict['current']
        if total >0:
            data = jso_dict['data']
            for line in data:
                item = NewsSimpleItem()
                #日期
                item['newsdate'] = line[0]
                #tmp
                # item['Tmp'] = line[1]
                # 标题
                item['simpletext'] = line[2].strip()
                # 网址
                item['newsurl'] = line[3]
                # 股票号
                item['symbol'] = line[4][2:]
                # yield item
                pageurl = item['newsurl'].strip()
                if pageurl.startswith('http://tech.qq.com'):
                    yield Request(pageurl, meta={'parent': item},callback=parse_tech_page)
                elif pageurl.startswith('http://stock.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_stock_page)
                elif pageurl.startswith('http://finance.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_finance_page)
                elif pageurl.startswith('http://news.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_news_page)
                else:
                    with open('url.txt','a',encoding='utf-8') as f:
                        f.write(pageurl + '\n')


            if total > current:
                code = jso_dict['data'][1][-1]
                nextpage = current + 1
                baseurl = "http://news.gtimg.cn/more.php?q={}&page={}&_du_r_t={}"
                jsonurl = baseurl.format(code,nextpage,str(random.random())[:-2])
                yield Request(jsonurl, callback=self.parse)
#.......................................

#redis 缓存
class RedisCache():

    def __init__(self,cachekey='news_lasttime'):
        self.redisclient = redis.Redis(host='10.11.9.7', port=6379, db=14, password='centos_data_123456')
        self.cachekey = cachekey

    def set_redis(self,symbol, obj):
        self.redisclient.hset(self.cachekey, symbol, pickle.dumps(obj))

    def get_redis(self,symbol):
        data = self.redisclient.hget(self.cachekey, symbol)
        return pickle.loads(data)
#从接口拿到当前股票新闻的最新时间
def get_news_lasttime(code):
    url = "https://www.xinbozhengquan.com/bussiness/news_service/query_news_last.json"
    data_dict = {"tagStock":[code]}

    datajsonstr = json.JSONEncoder().encode(data_dict)
    rsp= requests.post(url, datajsonstr)
    resultjson=json.JSONDecoder().decode(rsp.text)
    try:
        newstime = resultjson['data']['sourcetime']
        return newstime
    except:
        return ''

rediscache = RedisCache()
class TxNewsSpiderUpdate(scrapy.Spider):
    name = "tx_news_update"
    start_urls = get_start_urls(codes=get_All_Symbols())
    custom_settings = {
        'ITEM_PIPELINES': {
            'new_scrapy.pipelines.ServiceArticlePipeline': 100,
        },
    }

    def parse(self, response):
        code = urlparams(response.url)['q'][2:]
        lastdatetime= rediscache.get_redis(code)

        try:
            text = response.body.decode("gbk")
            jsontext = text.replace('var finance_news =','').replace("'",'"').strip()[:-1]
            jso_dict = json.loads(jsontext)
        except:
            url = response.url
            err_log('list',url)
            sys.exit(0)

        total = jso_dict['total']
        current = jso_dict['current']
        if total >0:
            data = jso_dict['data']
            for line in data:
                item = NewsSimpleItem()
                #日期
                item['newsdate'] = line[0]

                if item['newsdate'] <= lastdatetime:
                    print("............跳出..................")
                    break

                # 标题
                item['simpletext'] = line[2].strip()
                # 网址
                item['newsurl'] = line[3]
                # 股票号
                item['symbol'] = line[4][2:]
                # yield item
                pageurl = item['newsurl'].strip()
                if pageurl.startswith('http://tech.qq.com'):
                    yield Request(pageurl, meta={'parent': item},callback=parse_tech_page)
                elif pageurl.startswith('http://stock.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_stock_page)
                elif pageurl.startswith('http://finance.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_finance_page)
                elif pageurl.startswith('http://news.qq.com'):
                    yield Request(pageurl, meta={'parent': item}, callback=parse_news_page)
                else:
                    with open('url.txt','a',encoding='utf-8') as f:
                        f.write(pageurl + '\n')

            if total > current:
                code = jso_dict['data'][1][-1]
                nextpage = current + 1
                baseurl = "http://news.gtimg.cn/more.php?q={}&page={}&_du_r_t={}"
                jsonurl = baseurl.format(code,nextpage,str(random.random())[:-2])
                yield Request(jsonurl, callback=self.parse)

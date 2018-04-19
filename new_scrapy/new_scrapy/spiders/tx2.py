# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsSimpleItem
from ..items import NewsArticleItem
from bs4 import BeautifulSoup
import ast
import re
import redis
import requests
import json
import pickle
import sys
import time

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

def err_log(description,url):
    pass
    # with open('err.txt', 'a', encoding='utf-8') as f:
    #     f.write(description+":"+url+"\n")

# 生成起始url列表
def get_start_urls(codes=get_Dynamic_Symbols()):
    print("..............................................")
    for code in codes:
        try:
            rediscache.set_redis(code, get_news_lasttime(code))
            # baseurl = "http://news.gtimg.cn/more.php?q=us{}&page=1&_du_r_t={}".format(code, str(random.random())[:-2])
            baseurl = "http://web.ifzq.gtimg.cn/appstock/news/info/search?page=1&symbol=us{}&n=51&_var=finance_news&_appName=web&type=2&_appver=1.0&_={}"
            timestamp = int(time.time() * 1000)
            url = baseurl.format(code, timestamp)
            yield url
        except:
            print("..............")
            continue

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
            if ss.strip().startswith('var related_video_info ='):
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
            if ss.strip().startswith('var related_video_info ='):
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
            if ss.strip().startswith('var related_video_info ='):
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
            if ss.strip().startswith('var related_video_info ='):
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

#............................................
# 全量抓取的.......................
class TxNewsSpider2(scrapy.Spider):
    name = "tx_news_all2"
    start_urls = get_start_urls(codes=get_All_Symbols())
    custom_settings = {
        'MONGODB_SERVER': '10.11.9.7',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'newsdb',
        'MONGODB_COLLECTION': 'tx',

        'ITEM_PIPELINES': {
            'new_scrapy.pipelines.ServiceArticlePipeline': 100,
            # 'new_scrapy.pipelines.MongoDBPipeline': 200,

        },
    }

    def parse(self, response):
        url_params = urlparams(response.url)
        code = url_params['symbol'][2:]
        page_num = url_params['page']

        # lastdatetime = rediscache.get_redis(code)

        try:
            text = response.body_as_unicode()
            # jsontext = text.replace('finance_news=', '').replace("'", '"')
            jsontext = text.replace('finance_news=', '')
            jso_dict = json.loads(jsontext)
        except:
            url = response.url
            err_log('list', url)
            sys.exit(0)

        data = jso_dict['data']
        total_num = data['total_num']

        # current = jso_dict['current']
        if total_num > 0:
            flag = True
            lines = data['data']
            if lines != []:
                for line in lines:
                    item = NewsSimpleItem()
                    # 日期
                    item['newsdate'] = line['time']
                    # if item['newsdate'] <= lastdatetime:
                    #     flag = False
                    #     print("............跳出..................")
                    #     break

                    # 标题
                    item['simpletext'] = line['title']
                    # 网址
                    item['newsurl'] = line['url']
                    # 股票号
                    item['symbol'] = code
                    # yield item
                    pageurl = item['newsurl'].strip()
                    if pageurl.startswith('http://tech.qq.com'):
                        yield Request(pageurl, meta={'parent': item}, callback=parse_tech_page)
                    elif pageurl.startswith('http://stock.qq.com'):
                        yield Request(pageurl, meta={'parent': item}, callback=parse_stock_page)
                    elif pageurl.startswith('http://finance.qq.com'):
                        yield Request(pageurl, meta={'parent': item}, callback=parse_finance_page)
                    elif pageurl.startswith('http://news.qq.com'):
                        yield Request(pageurl, meta={'parent': item}, callback=parse_news_page)
                    else:
                        pass
                        # with open('url.txt','a',encoding='utf-8') as f:
                        #     f.write(pageurl + '\n')
            else:
                flag = False
            if flag:
                code = code
                nextpage = int(page_num) + 1
                baseurl = "http://web.ifzq.gtimg.cn/appstock/news/info/search?page={}&symbol=us{}&n=51&_var=finance_news&_appName=web&type=2&_appver=1.0&_={}"
                timestamp = int(time.time() * 1000)
                url = baseurl.format(nextpage, code, timestamp)
                yield Request(url, callback=self.parse)
#.................................................

#redis 缓存
class RedisCache():

    def __init__(self,cachekey='news_lasttime'):
        # self.redisclient = redis.Redis(host='r-2ze4635ef679bf64.redis.rds.aliyuncs.com', port=6379, db=2, password='rootdB2017')
        self.redisclient = redis.Redis(host='39.106.168.88', port=6379, db=3, password='ygkjtest')
        # self.redisclient = redis.Redis(host='127.0.0.1', port=6379, db=2)

        self.cachekey = cachekey

    def set_redis(self,symbol, obj):
        self.redisclient.hset(self.cachekey, symbol, pickle.dumps(obj))

    def get_redis(self,symbol):
        data = self.redisclient.hget(self.cachekey, symbol)
        return pickle.loads(data)
#从接口拿到当前股票新闻的最新时间
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

rediscache = RedisCache()
class TxNewsSpiderUpdate2(scrapy.Spider):
    name = "tx_news_update2"
    # start_urls = get_start_urls(codes=get_All_Symbols())
    start_urls = get_start_urls(codes=['PPDF',])
    # start_urls = get_start_urls(codes=['LX'])
    custom_settings = {

        'MONGODB_SERVER':'10.11.9.7',
        'MONGODB_PORT':27017,
        'MONGODB_DB':'newsdb',
        'MONGODB_COLLECTION':'tx',

        'ITEM_PIPELINES': {
            'new_scrapy.pipelines.ServiceArticlePipeline': 100,
            # 'new_scrapy.pipelines.MongoDBPipeline': 200,

        },
    }

    def parse(self, response):
        url_params = urlparams(response.url)
        code = url_params['symbol'][2:]
        print(code)
        page_num = url_params['page']

        lastdatetime= rediscache.get_redis(code)

        try:
            text = response.body_as_unicode()

            # jsontext = text.replace('finance_news=', '').replace("'", '"')
            jsontext = text.replace('finance_news=', '')
            jso_dict = json.loads(jsontext)
        except:
            url = response.url
            err_log('list',url)
            sys.exit(0)

        data = jso_dict['data']
        total_num = data['total_num']

        # current = jso_dict['current']
        if total_num >0:
            flag = True

            lines = data['data']
            if lines != []:
                for line in lines:
                    item = NewsSimpleItem()
                    #日期
                    item['newsdate'] = line['time']

                    if item['newsdate'] <= lastdatetime:
                        flag = False
                        print("............跳出..................")
                        break

                    # 标题
                    item['simpletext'] = line['title']
                    # 网址
                    item['newsurl'] = line['url']
                    # 股票号
                    item['symbol'] = code
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
                        pass
                        # with open('url.txt','a',encoding='utf-8') as f:
                        #     f.write(pageurl + '\n')
            else:
                flag = False

            if flag:
                code = code
                nextpage = int(page_num) + 1
                baseurl = "http://web.ifzq.gtimg.cn/appstock/news/info/search?page={}&symbol=us{}&n=51&_var=finance_news&_appName=web&type=2&_appver=1.0&_={}"
                timestamp = int(time.time() * 1000)
                url = baseurl.format(nextpage,code, timestamp)
                yield Request(url, callback=self.parse)

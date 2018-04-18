# -*- coding: utf-8 -*-
import scrapy
import redis
import json
import time
import requests
from ..items.xueqiuitems import BaseItem
from ..xueqiu.xueqiu import Downloader
from ..utils.code_tools import get_Dynamic_Symbols,get_All_Symbols,get_Code_List_List

codelist = get_All_Symbols()

def getUrls(codes=codelist):
    codes_n = get_Code_List_List(codes)
    for code_l in codes_n:
        url = "https://xueqiu.com/v4/stock/quote.json?code=" + ",".join(code_l)
        yield url

def getXignite(symbol):
    url = "https://globalquotes.xignite.com/v3/xGlobalQuotes.json/GetGlobalDelayedQuote?IdentifierType=Symbol&Identifier={}&_token=B1FB744B5FB04B0AB40E45D531D06876".format(symbol)
    rsp = requests.get(url)
    xignite_json_data = rsp.json()
    return xignite_json_data
    # print(json_data['High52Weeks'])
    # print(json_data['Low52Weeks'])

def getXigniteList(symbols):
    baseurl = "https://globalquotes.xignite.com/v3/xGlobalQuotes.json/GetGlobalDelayedQuotes?IdentifierType=Symbol&Identifiers={}&_token=B1FB744B5FB04B0AB40E45D531D06876"
    url = baseurl.format(','.join(symbols))
    rsp = requests.get(url)
    xignite_json_data = rsp.json()
    return_data = {}
    for line in xignite_json_data:
        return_data[line['Security']['Symbol']] = line
    return return_data
    # return xignite_json_data
    # print(json_data['High52Weeks'])
    # print(json_data['Low52Weeks'])

def url2params(url):
    tmp = url.split('?')[-1]
    n_and_v = tmp.split('&')
    params = {}
    for line in n_and_v:
        tmp = line.split('=')
        params[tmp[0]] = tmp[1]
    return params

class Week52BaseXueQiuXigniteSpider(scrapy.Spider):
    name = "week52base_xueqiu_xignite"
    allowed_domains = ["xueqiu.com"]
    # start_urls = ['http://xueqiu.com/']
    start_urls = getUrls()

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            # 'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }

    def parse(self, response):
        url = response.url
        jso_dict = json.loads(response.body_as_unicode())
        for k, v in jso_dict.items():
            #基本面的
            baseitem = BaseItem()
            # 代码
            baseitem['symbol'] = v['symbol']

            # 市盈率TTM
            baseitem['pe_ttm'] = v['pe_ttm']
            # 总市值
            baseitem['marketCapital'] = v['marketCapital']

            # xignite 的 52 周 最高最低 .............................
            xignite_json = getXignite(baseitem['symbol'])
            # 成功了 用xignite 的数据源
            if xignite_json['Outcome'] == 'Success':
                # 52周最高
                baseitem['high52week'] = xignite_json['High52Weeks']
                # 52周最低
                baseitem['low52week'] = xignite_json['Low52Weeks']
            # 不成功,雪球的数据源
            else:
                # 52周最高
                baseitem['high52week'] = v['high52week']
                # 52周最低
                baseitem['low52week'] = v['low52week']

            # # 中文名称
            # baseitem['name'] = v['name']
            # # 交易所
            # baseitem['exchange'] = v['exchange']
            #
            # # 总股本
            # baseitem['totalShares'] = v['totalShares']

            # # 市净率
            # baseitem['pb'] = v['pb']
            # # 市销率TTM
            # baseitem['psr'] = v['psr']
            # # 每股收益
            # baseitem['eps'] = v['eps']
            # # 每股净资产
            # baseitem['net_assets'] = v['net_assets']
            # # 股息
            # baseitem['dividend'] = v['dividend']
            # # 股息收益率
            # baseitem['yield_'] = v['yield']
            # # 机构持股比例
            # baseitem['instOwn'] = v['instOwn']
            # # 空头回补天数
            # baseitem['short_ratio'] = v['short_ratio']
            # # 机构持股比例
            # tim = v['time']
            # ti = tim[:-10] + tim[-4:]
            # ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            # ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            # baseitem['time'] = ti
            # print(baseitem)
            yield baseitem

class Week52BaseXueQiuXigniteSpider2(scrapy.Spider):
    name = "week52base2_xueqiu_xignite"
    allowed_domains = ["xueqiu.com"]
    # start_urls = ['http://xueqiu.com/']
    start_urls = getUrls()

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            # 'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }


    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        url = response.url
        params = url2params(url)
        symbols_list = params['code'].split(',')
        xignite_data = getXigniteList(symbols_list)
        for k, v in jso_dict.items():
            #基本面的
            baseitem = BaseItem()
            # 代码
            symbol = v['symbol']
            baseitem['symbol'] = symbol

            # 市盈率TTM
            baseitem['pe_ttm'] = v['pe_ttm']
            # 总市值
            baseitem['marketCapital'] = v['marketCapital']

            # xignite 的 52 周 最高最低 .............................
            xignite_single = xignite_data[symbol]
            # 成功了 用xignite 的数据源
            if xignite_single['Outcome'] == 'Success':
                # 52周最高
                baseitem['high52week'] = xignite_single['High52Weeks']
                # 52周最低
                baseitem['low52week'] = xignite_single['Low52Weeks']
            # 不成功,雪球的数据源
            else:
                # 52周最高
                baseitem['high52week'] = v['high52week']
                # 52周最低
                baseitem['low52week'] = v['low52week']

            # # 中文名称
            # baseitem['name'] = v['name']
            # # 交易所
            # baseitem['exchange'] = v['exchange']
            #
            # # 总股本
            # baseitem['totalShares'] = v['totalShares']

            # # 市净率
            # baseitem['pb'] = v['pb']
            # # 市销率TTM
            # baseitem['psr'] = v['psr']
            # # 每股收益
            # baseitem['eps'] = v['eps']
            # # 每股净资产
            # baseitem['net_assets'] = v['net_assets']
            # # 股息
            # baseitem['dividend'] = v['dividend']
            # # 股息收益率
            # baseitem['yield_'] = v['yield']
            # # 机构持股比例
            # baseitem['instOwn'] = v['instOwn']
            # # 空头回补天数
            # baseitem['short_ratio'] = v['short_ratio']
            # # 机构持股比例
            # tim = v['time']
            # ti = tim[:-10] + tim[-4:]
            # ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            # ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            # baseitem['time'] = ti
            print(baseitem)
            yield baseitem

# codelist = ["ALO"]
def getXigniteUrl(codes = codelist):
    codes_n = get_Code_List_List(codes)
    for code_l in codes_n:
        baseurl = "https://globalquotes.xignite.com/v3/xGlobalQuotes.json/GetGlobalDelayedQuotes?IdentifierType=Symbol&Identifiers={}&_token=B1FB744B5FB04B0AB40E45D531D06876"
        url = baseurl.format(",".join(code_l))
        yield url

class Week52BaseXigniteXueQiuSpider(scrapy.Spider):
    name = "week52base_xignite_xueqiu"
    allowed_domains = ["xueqiu.com"]
    # start_urls = ['http://xueqiu.com/']
    start_urls = getXigniteUrl()

    custom_settings = {

        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }

    def __init__(self):
        self.xueqiu_downloader = Downloader()
    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        url = response.url
        params = url2params(url)
        symbols_list = params['Identifiers'].split(',')
        xueqiu_data = self.xueqiu_downloader.download(symbols_list)
        for line in jso_dict:
            #基本面的
            baseitem = BaseItem()

            # 代码
            symbol = line['Security']['Symbol']
            baseitem['symbol'] = symbol

            xueqiu_line = xueqiu_data.get(symbol,{})
            # 市盈率TTM
            baseitem['pe_ttm'] = xueqiu_line.get('pe_ttm','')
            # 总市值
            baseitem['marketCapital'] = xueqiu_line.get('marketCapital','')

            # xignite 的 52 周 最高最低 .............................
            # 成功了 用xignite 的数据源
            if line['Outcome'] == 'Success':
                # 52周最高
                baseitem['high52week'] = line['High52Weeks']
                # 52周最低
                baseitem['low52week'] = line['Low52Weeks']
            # 不成功,雪球的数据源
            else:
                # 52周最高
                baseitem['high52week'] = xueqiu_line.get('high52week','')
                # 52周最低
                baseitem['low52week'] = xueqiu_line.get('low52week','')

            # # 中文名称
            # baseitem['name'] = v['name']
            # # 交易所
            # baseitem['exchange'] = v['exchange']
            #
            # # 总股本
            # baseitem['totalShares'] = v['totalShares']

            # # 市净率
            # baseitem['pb'] = v['pb']
            # # 市销率TTM
            # baseitem['psr'] = v['psr']
            # # 每股收益
            # baseitem['eps'] = v['eps']
            # # 每股净资产
            # baseitem['net_assets'] = v['net_assets']
            # # 股息
            # baseitem['dividend'] = v['dividend']
            # # 股息收益率
            # baseitem['yield_'] = v['yield']
            # # 机构持股比例
            # baseitem['instOwn'] = v['instOwn']
            # # 空头回补天数
            # baseitem['short_ratio'] = v['short_ratio']
            # # 机构持股比例
            # tim = v['time']
            # ti = tim[:-10] + tim[-4:]
            # ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            # ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            # baseitem['time'] = ti
            print(baseitem)
            yield baseitem


# -*- coding: utf-8 -*-
import json
import redis
import time
from ..scrapy_redis.spiders import RedisCrawlSpider
from ..items.xueqiuitems import SnapshotItem,BaseItem

class XueqiuRedisSpider(RedisCrawlSpider):
    name = "xueqiu_redis"
    redis_key = 'xueqiu_redis:start_urls'
    custom_settings = {

        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }
    def __init__(self,*args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(XueqiuRedisSpider, self).__init__(*args, **kwargs)

        # self.taskclient = redis.Redis(host='10.11.9.7',port=6379,db=0,password='centos_data_123456')
        self.taskclient = redis.Redis(host='10.11.9.12',port=6379,db=0,password='foobared')

        self.index_list = ['SP500', 'DJI30']

    def parse(self, response):
        url = response.url
        self.taskclient.rpush('xueqiu_redis:start_urls', url)
        jso_dict = json.loads(response.body_as_unicode())
        for k, v in jso_dict.items():
            item = SnapshotItem()
            # 股票代码
            item['CODE'] = v['symbol']
            # 成交时间
            item['DEALTIME'] = v['time']
            # 现价
            item['PRICE'] = v['current']
            # 今开
            item['OPEN'] = v['open']
            # 收盘
            item['CLOSE'] = v['close']
            # 最高
            item['HIGH'] = v['high']
            # 最低
            item['LOW'] = v['low']
            # 昨收
            item['PREV'] = v['last_close']
            # 成交额
            # item['VALUE'] = v['symbol']
            # 成交量
            item['VOLUME'] = float(v['volume'])
            # 买1
            # item['BP1'] = v['symbol']
            # 卖1
            # item['SP1'] = v['symbol']
            # 买量1
            # item['BV1'] = v['symbol']
            # 卖量1
            # item['SV1'] = v['symbol']
            # 假数据
            # 买1
            item['BP1'] = round(float(item['PRICE']) * (1 - 0.01), 2)
            # 卖1
            item['SP1'] = round(float(item['PRICE']) * (1 + 0.01), 2)
            # 买量1
            item['BV1'] = 100
            # 卖量1
            item['SV1'] = 100

            if item['CODE'] in self.index_list:
                yield item

            #基本面的
            baseitem = BaseItem()
            # 中文名称
            baseitem['name'] = v['name']
            # 交易所
            baseitem['exchange'] = v['exchange']
            # 代码
            baseitem['symbol'] = v['symbol']
            # 总市值
            baseitem['marketCapital'] = v['marketCapital']
            # 市盈率TTM
            baseitem['pe_ttm'] = v['pe_ttm']
            # 总股本
            baseitem['totalShares'] = v['totalShares']
            # 52周最高
            baseitem['high52week'] = v['high52week']
            # 52周最低
            baseitem['low52week'] = v['low52week']
            # 市净率
            baseitem['pb'] = v['pb']
            # 市销率TTM
            baseitem['psr'] = v['psr']
            # 每股收益
            baseitem['eps'] = v['eps']
            # 每股净资产
            baseitem['net_assets'] = v['net_assets']
            # 股息
            baseitem['dividend'] = v['dividend']
            # 股息收益率
            baseitem['yield_'] = v['yield']
            # 机构持股比例
            baseitem['instOwn'] = v['instOwn']
            # 空头回补天数
            baseitem['short_ratio'] = v['short_ratio']
            # 机构持股比例
            tim = v['time']
            ti = tim[:-10] + tim[-4:]
            ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            baseitem['time'] = ti

            yield baseitem

class XueqiuRedisSpiderSnopshot(RedisCrawlSpider):
    name = "xueqiu_snopshot_redis"
    redis_key = 'xueqiu_snopshot_redis:start_urls'
    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_kuaizhao',

        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }
    def __init__(self,*args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(XueqiuRedisSpider, self).__init__(*args, **kwargs)

        # self.taskclient = redis.Redis(host='10.11.9.7',port=6379,db=0,password='centos_data_123456')
        self.taskclient = redis.Redis(host='10.11.9.12',port=6379,db=0,password='foobared')

    def parse(self, response):
        url = response.url
        self.taskclient.rpush('xueqiu_redis:start_urls', url)
        jso_dict = json.loads(response.body_as_unicode())
        for k, v in jso_dict.items():
            item = SnapshotItem()
            # 股票代码
            item['CODE'] = v['symbol']
            # 成交时间
            item['DEALTIME'] = v['time']
            # 现价
            item['PRICE'] = v['current']
            # 今开
            item['OPEN'] = v['open']
            # 收盘
            item['CLOSE'] = v['close']
            # 最高
            item['HIGH'] = v['high']
            # 最低
            item['LOW'] = v['low']
            # 昨收
            item['PREV'] = v['last_close']
            # 成交额
            # item['VALUE'] = v['symbol']
            # 成交量
            item['VOLUME'] = float(v['volume'])
            # 买1
            # item['BP1'] = v['symbol']
            # 卖1
            # item['SP1'] = v['symbol']
            # 买量1
            # item['BV1'] = v['symbol']
            # 卖量1
            # item['SV1'] = v['symbol']
            # 假数据
            # 买1
            item['BP1'] = round(float(item['PRICE']) * (1 - 0.01), 2)
            # 卖1
            item['SP1'] = round(float(item['PRICE']) * (1 + 0.01), 2)
            # 买量1
            item['BV1'] = 100
            # 卖量1
            item['SV1'] = 100

            yield item

class XueqiuRedisSpiderBase(RedisCrawlSpider):
    name = "xueqiu_base_redis"
    redis_key = 'xueqiu_base_redis:start_urls'
    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_kuaizhao',

        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
        'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES':{
            'data_scrapy_redis.pipelines.xueqiu_pipelines.XueQiuRedisStorePipeline': 100,
            #'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }
    def __init__(self,*args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(XueqiuRedisSpider, self).__init__(*args, **kwargs)

        # self.taskclient = redis.Redis(host='10.11.9.7',port=6379,db=0,password='centos_data_123456')
        self.taskclient = redis.Redis(host='10.11.9.12',port=6379,db=0,password='foobared')

    def parse(self, response):
        url = response.url
        self.taskclient.rpush('xueqiu_redis:start_urls', url)
        jso_dict = json.loads(response.body_as_unicode())
        for k, v in jso_dict.items():
            #基本面的
            baseitem = BaseItem()
            # 中文名称
            baseitem['name'] = v['name']
            # 交易所
            baseitem['exchange'] = v['exchange']
            # 代码
            baseitem['symbol'] = v['symbol']
            # 总市值
            baseitem['marketCapital'] = v['marketCapital']
            # 市盈率TTM
            baseitem['pe_ttm'] = v['pe_ttm']
            # 总股本
            baseitem['totalShares'] = v['totalShares']
            # 52周最高
            baseitem['high52week'] = v['high52week']
            # 52周最低
            baseitem['low52week'] = v['low52week']
            # 市净率
            baseitem['pb'] = v['pb']
            # 市销率TTM
            baseitem['psr'] = v['psr']
            # 每股收益
            baseitem['eps'] = v['eps']
            # 每股净资产
            baseitem['net_assets'] = v['net_assets']
            # 股息
            baseitem['dividend'] = v['dividend']
            # 股息收益率
            baseitem['yield_'] = v['yield']
            # 机构持股比例
            baseitem['instOwn'] = v['instOwn']
            # 空头回补天数
            baseitem['short_ratio'] = v['short_ratio']
            # 机构持股比例
            tim = v['time']
            ti = tim[:-10] + tim[-4:]
            ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            baseitem['time'] = ti

            yield baseitem


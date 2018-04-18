# -*- coding: utf-8 -*-
import json
import redis
import time
from ..scrapy_redis.spiders import RedisCrawlSpider
from ..items.xueqiuitems import MinItem

class XueqiuRedisSpider(RedisCrawlSpider):
    name = "xueqiu_min_redis"
    redis_key = 'xueqiu_min_redis:start_urls'

    custom_settings = {

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
            'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
            'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES': {
            'data_scrapy_redis.pipelines.xueqiu_min_piplines.XueQiuMinRedisStorePipeline': 100,
        },
    }

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(XueqiuRedisSpider, self).__init__(*args, **kwargs)

        # self.taskclient = redis.Redis(host='10.11.9.7',port=6379,db=0,password='centos_data_123456')
        self.taskclient = redis.Redis(host='10.11.9.12', port=6379, db=0, password='foobared')

    def parse(self, response):
        url = response.url
        self.taskclient.rpush('xueqiu_min_redis:start_urls', url)
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist']
        mink = {}
        mink['symbol'] = symbol
        datelist = []
        for line_dict in chartlist:
            item = MinItem()
            item['symbol'] = symbol
            # 当前价
            item['current'] = line_dict['current']
            # 成交均价
            item['avg_price'] = line_dict['avg_price']
            # 成交量
            item['volume'] = line_dict['volume']
            # 美国时间
            ss = line_dict['time']
            ss = ss[:-10] + ss[-4:]
            ti = time.strptime(ss, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            datelist.append(item)
        mink['datelist'] = datelist
        return mink
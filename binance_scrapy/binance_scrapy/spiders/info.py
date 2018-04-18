# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup

class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['binance.com']
    # start_urls = ["https://info.binance.com/en/","https://info.binance.com/cn/"]
    start_urls = ["https://info.binance.com/en/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
            'binance_scrapy.middlewares.ProxyMiddleware': 100,
        },

        # 'ITEM_PIPELINES': {
        #     # 'sec_scrapy.pipelines.MongoDBPipeline': 100,
        #     'data_scrapy_redis.pipelines.sec_pipelines.MySQLDBPipeline': 200,
        # },
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        body = soup.find('tbody')
        trs = body.find_all('tr', recursive=False)

        base_url = 'https://info.binance.com{}'
        for tr in trs:
            url = base_url.format(tr.get('link'))
            yield Request(url, callback=self.parse_document, dont_filter=True)

    def parse_document(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        print(soup)
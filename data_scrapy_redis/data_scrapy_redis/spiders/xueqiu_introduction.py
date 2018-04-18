#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/8 15:18
# @Author  : zhujinghui
# @File    : xueqiu_introduction.py
# @Software: PyCharm
import scrapy
from bs4 import BeautifulSoup
from ..items.xueqiuitems import IntroductionItem
from ..utils.code_tools import get_Dynamic_Symbols,get_All_Symbols
codes = get_Dynamic_Symbols()
def geUrl():
    for code in codes:
        url = "https://xueqiu.com/S/{}".format(code)
        yield url
class XueqiuSpider_StockIntroduction(scrapy.Spider):
    name = "xueqiu_introduction"
    allowed_domains = ["xueqiu.com"]
    start_urls = geUrl()
    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stocks_base',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE': 'stocks_base',

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
            'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
            # 'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
            # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES': {
            # 'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_base': 100
                           },
    }
    def parse(self, response):
        text = response.body_as_unicode()
        soup = BeautifulSoup(text,'lxml')
        item = IntroductionItem()

        introduction = soup.find('div', class_='profile-detail hide')

        detail = introduction.next_element
        item['detail'] = detail


        website = introduction.find(text='公司网站：')
        if website:
            item['website'] = website.next_element.text

        telphone = introduction.find(text='公司电话：')
        if telphone:
            item['website'] = telphone.next_element

        address = introduction.find(text='公司地址：')
        if address:
            item['address'] = address.next_element

        prospectus = introduction.find(text='招股说明书：')
        if prospectus:
            item['prospectus'] = prospectus.next_element.get('href')

        print(item)
        # yield item

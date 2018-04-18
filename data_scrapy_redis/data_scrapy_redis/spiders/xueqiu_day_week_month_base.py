#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 16:14
# @Author  : zhujinghui
# @File    : xueqiu_day_week_month.py
# @Software: PyCharm
import scrapy
import datetime
import redis
import json
import time
from dateutil.relativedelta import relativedelta
from ..items.xueqiuitems import DayItem,WeekItem,MonthItem,BaseItem

def getCodeSet(keyname = "symbols400"):
    client = redis.Redis(host='10.9.210.109', port=6390, db=0, password='ygkj', decode_responses=True)
    codeset = client.smembers(keyname)
    return codeset

#日k抓取
def getUrlList_all():
    now = datetime.datetime.now()
    end = now + datetime.timedelta(- 1)
    end = end.replace(hour=12, minute=0, second=0, microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1day&end={}&type=normal&symbol={}".format(endstamp,code)
        yield url

def getUrlList_current():
    now = datetime.datetime.now()
    end = now + datetime.timedelta(- 1)
    end = end.replace(hour=12, minute=0, second=0, microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    begin = end + datetime.timedelta(- 1)
    beginstamp = str(int(begin.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=normal&begin={}&end={}&_={}".format(code,beginstamp,endstamp,endstamp)
        yield url

class XueqiuaySpiderAll(scrapy.Spider):
    name = "xueqiu_day_all"
    allowed_domains = ["xueqiu.com"]
    start_urls = getUrlList_all()

    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },
    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist']
        for line_dict in chartlist:
            item = DayItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']
            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

class XueqiuaySpiderCurrent(scrapy.Spider):
    name = "xueqiu_day_current"
    allowed_domains = ["xueqiu.com"]
    start_urls = getUrlList_current()

    custom_settings = {

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE' : 'stock_dayk',

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },

    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist']
        for line_dict in chartlist:
            item = DayItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']
            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

#周k抓取
def getWeekUrlList_all():
    now = datetime.datetime.now()
    end = now + datetime.timedelta(- now.isoweekday())
    end = end.replace(hour=12,minute=0,second=0,microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    year = now.year - 4
    begin = now.replace(year=year)
    beginstamp = str(int(begin.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        # url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1week&type=normal&begin=" + beginstamp + "&end=" + endstamp + "&symbol=" + code
        # url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1week&type=normal&symbol={}".format(code)
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1week&type=normal&begin={}&end={}&symbol={}".format(beginstamp,endstamp,code)
        yield url

def getWeekUrlList_last():
    now = datetime.datetime.now()
    end = now + datetime.timedelta(- now.isoweekday())
    end = end.replace(hour=12, minute=0, second=0, microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    begin = end + datetime.timedelta(- 21)
    beginstamp = str(int(begin.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1week&type=normal&begin={}&end={}&symbol={}".format(beginstamp,endstamp,code)
        yield url

class XueqiuayWeekSpiderAll(scrapy.Spider):
    name = "xueqiu_week_all"
    allowed_domains = ["xueqiu.com"]
    start_urls = getWeekUrlList_all()

    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_weekk',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE' : 'stock_weekk',

         'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },
    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist']
        for line_dict in chartlist:
            item = WeekItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']
            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

class XueqiuayWeekSpiderCurrent(scrapy.Spider):
    name = "xueqiu_week_current"
    allowed_domains = ["xueqiu.com"]
    start_urls = getWeekUrlList_last()

    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_weekk',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE': 'stock_weekk',

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },
    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist'][-1:]
        for line_dict in chartlist:
            item = WeekItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']

            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

# 月k抓取
def getMonthUrlList_all():
    now = datetime.datetime.now()

    end = now + datetime.timedelta(- now.day)
    end = end.replace(hour=12, minute=0, second=0, microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol=" + code + "&period=1month&type=normal&end=" + endstamp + "&_=" + endstamp
        yield url

def getMonthUrlList_last():
    now = datetime.datetime.now()

    end = now + datetime.timedelta(- now.day)
    end = end.replace(hour=12, minute=0, second=0, microsecond=0)
    endstamp = str(int(end.timestamp()) * 1000)

    begin = end - relativedelta(months=+4)
    #begin = end + datetime.timedelta(- 27)
    beginstamp = str(int(begin.timestamp()) * 1000)

    code_list = getCodeSet()
    for code in code_list:
        url = "https://xueqiu.com/stock/forchartk/stocklist.json?period=1month&type=normal&begin={}&end={}&symbol={}".format(beginstamp,endstamp,code)
        yield url

class XueqiuayMonthSpiderAll(scrapy.Spider):
    name = "xueqiu_month_all"
    allowed_domains = ["xueqiu.com"]
    start_urls = getMonthUrlList_all()

    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_monthk',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE': 'stock_monthk',

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },
    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist']
        for line_dict in chartlist:
            item = MonthItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']
            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

class XueqiuayMonthSpiderCurrent(scrapy.Spider):
    name = "xueqiu_month_current"
    allowed_domains = ["xueqiu.com"]
    start_urls = getMonthUrlList_last()

    custom_settings = {
        # 'MYSQL_HOST': '10.9.210.109',
        # 'MYSQL_DBNAME': 'ra_online',
        # 'MYSQL_USER': 'liangxiang',
        # 'MYSQL_PASSWD': 'lx_2017_xhyg',
        # 'MYSQL_TABLE': 'stock_monthk',

        'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
        'MYSQL_DBNAME': 'xhyg_us_stocks',
        'MYSQL_USER': 'yigukeji_db',
        'MYSQL_PASSWD': 'Yigukeji_dba',
        'MYSQL_TABLE': 'stock_monthk',

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_day_week_month': 100
        },
    }

    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        symbol = jso_dict['stock']['symbol']
        chartlist = jso_dict['chartlist'][-1]
        # ret_dict = {}
        # ret_list = []
        for line_dict in chartlist:
            item = MonthItem()
            # 股票号
            item['symbol'] = symbol
            # 开盘价
            item['open'] = line_dict['open']
            # 最高价
            item['high'] = line_dict['high']
            # 最低价
            item['low'] = line_dict['low']
            # 收盘价
            item['close'] = line_dict['close']
            # 成交量
            item['volume'] = line_dict['volume']
            # 涨跌幅
            item['percent'] = line_dict['percent']
            # 换手率
            item['turnrate'] = line_dict['turnrate']
            # 数据时间戳 , 美国时间
            v = line_dict['time']
            v = v[:-10] + v[-4:]
            ti = time.strptime(v, "%a %b %d %H:%M:%S  %Y")
            v = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = v
            yield item

#基本面更新
def get_Code_List_List(code_list,n=50):
    list_list = []
    for i in range(0, len(code_list), n):
        list_list.append(code_list[i:i + n])
    return list_list
def getUrlList():
    code_list = list(getCodeSet())
    code_list_list = get_Code_List_List(code_list)
    for code50 in code_list_list:
        url = "https://xueqiu.com/v4/stock/quote.json?code=" + ",".join(code50)
        yield url

class XueqiuSpider_base(scrapy.Spider):
    name = "xueqiu_base"
    allowed_domains = ["xueqiu.com"]
    start_urls = getUrlList()
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

        'ITEM_PIPELINES': {
            'dbf_scrapy_redis.pipelines.xueqiu_day_week_month_base_piplines.MySQLStorePipeline_base': 100
                           },
    }
    def parse(self, response):
        jso_dict = json.loads(response.body_as_unicode())
        for k,v in jso_dict.items():
            item = BaseItem()
            # 中文名称
            item['name'] = v['name']
            # 交易所
            item['exchange'] = v['exchange']
            # 代码
            item['symbol'] = v['symbol']
            # 总市值
            item['marketCapital'] = v['marketCapital']
            # 市盈率TTM
            item['pe_ttm'] = v['pe_ttm']
            # 总股本
            item['totalShares'] = v['totalShares']
            # 52周最高
            item['high52week'] = v['high52week']
            # 52周最低
            item['low52week'] = v['low52week']
            # 市净率
            item['pb'] = v['pb']
            # 市销率TTM
            item['psr'] = v['psr']
            # 每股收益
            item['eps'] = v['eps']
            # 每股净资产
            item['net_assets'] = v['net_assets']
            # 股息
            item['dividend'] = v['dividend']
            # 股息收益率
            item['yield_'] = v['yield']
            # 机构持股比例
            item['instOwn'] = v['instOwn']
            # 空头回补天数
            item['short_ratio'] = v['short_ratio']
            # 机构持股比例
            tim = v['time']
            ti = tim[:-10] + tim[-4:]
            ti = time.strptime(ti, "%a %b %d %H:%M:%S  %Y")
            ti = time.strftime("%Y-%m-%d %H:%M:%S", ti)
            item['time'] = ti

            yield item


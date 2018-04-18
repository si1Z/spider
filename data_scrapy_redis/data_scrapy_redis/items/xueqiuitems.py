#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/12 14:05
# @Author  : zhujinghui
# @File    : xueqiu.py
# @Software: PyCharm
import scrapy

#快照定义字段
class SnapshotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #股票代码
    CODE = scrapy.Field()

    #成交时间
    DEALTIME = scrapy.Field()

    #现价
    PRICE = scrapy.Field()

    #今开
    OPEN = scrapy.Field()

    #收盘
    CLOSE = scrapy.Field()

    #最高
    HIGH = scrapy.Field()

    #最低
    LOW = scrapy.Field()

    #昨收
    PREV = scrapy.Field()

    #成交额
    VALUE = scrapy.Field()
    #成交量
    VOLUME = scrapy.Field()

    #买1
    BP1 = scrapy.Field()

    #卖1
    SP1 = scrapy.Field()

    #买量1
    BV1 = scrapy.Field()

    #卖量1
    SV1 = scrapy.Field()
 #分时定义字段

#基本信息定义字段
class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 中文名称
    name = scrapy.Field()
    # 交易所
    exchange = scrapy.Field()
    # 代码
    symbol = scrapy.Field()
    # 总市值
    marketCapital = scrapy.Field()
    # 市盈率TTM
    pe_ttm = scrapy.Field()
    # 总股本
    totalShares = scrapy.Field()
    # 52周最高
    high52week = scrapy.Field()
    # 52周最低
    low52week = scrapy.Field()
    # 市净率
    pb = scrapy.Field()
    # 市销率TTM
    psr = scrapy.Field()
    # 每股收益
    eps = scrapy.Field()
    # 每股净资产
    net_assets = scrapy.Field()
    # 股息
    dividend = scrapy.Field()
    # 股息收益率
    yield_ = scrapy.Field()
    # 机构持股比例
    instOwn = scrapy.Field()
    #  空头回补天数
    short_ratio = scrapy.Field()
    # 时间戳
    time  = scrapy.Field()

#分时定义字段
class MinItem(scrapy.Item):
    #股票代码
    symbol = scrapy.Field()
    # 当前价
    current = scrapy.Field()
    # 成交均价
    avg_price = scrapy.Field()
    # 成交量
    volume = scrapy.Field()
    # 时间
    time = scrapy.Field()

#日k定义字段
class DayItem(scrapy.Item):
    # 股票代码
    symbol = scrapy.Field()
    # 开盘价
    open = scrapy.Field()
    # 最高价
    high = scrapy.Field()
    # 最低价
    low = scrapy.Field()
    # 收盘价
    close = scrapy.Field()
    # 前复权价格
    close_fa = scrapy.Field()
    # 后复权价格
    close_ba= scrapy.Field()
    # 成交量
    volume = scrapy.Field()
    # 涨跌幅
    percent = scrapy.Field()
    # 换手率
    turnrate = scrapy.Field()
    # 美国时间
    time = scrapy.Field()

#周k定义字段
class WeekItem(scrapy.Item):
    # 股票代码
    symbol = scrapy.Field()
    # 开盘价
    open = scrapy.Field()
    # 最高价
    high = scrapy.Field()
    # 最低价
    low = scrapy.Field()
    # 收盘价
    close = scrapy.Field()
    # 成交量
    volume = scrapy.Field()
    # 涨跌幅
    percent = scrapy.Field()
    # 换手率
    turnrate = scrapy.Field()
    # 美国时间
    time = scrapy.Field()

#月k定义字段
class MonthItem(scrapy.Item):
    # 股票代码
    symbol = scrapy.Field()
    # 开盘价
    open = scrapy.Field()
    # 最高价
    high = scrapy.Field()
    # 最低价
    low = scrapy.Field()
    # 收盘价
    close = scrapy.Field()
    # 成交量
    volume = scrapy.Field()
    # 涨跌幅
    percent = scrapy.Field()
    # 换手率
    turnrate = scrapy.Field()
    # 美国时间
    time = scrapy.Field()


#公司介绍
class IntroductionItem(scrapy.Item):
    # 详情
    detail = scrapy.Field()
    # 公司网站
    website = scrapy.Field()
    # 公司地址
    address = scrapy.Field()
    # 电话
    telphone = scrapy.Field()
    #招股说明书
    prospectus = scrapy.Field()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 下午4:20
# @Author  : zhujinghui 
# @site    : 
# @File    : bit_model.py
# @Software: PyCharm

from sqlalchemy import Column,String,Integer,DateTime,Boolean
from . import Base

class CoinMarketCap(Base):
    __tablename__ = 'coinmarketcap'

    # 行号，没用
    # num = scrapy.Field()
    # 英文名
    ename = Column(String(50),primary_key=True,nullable=True,comment='英文名')
    # 代码 有可能有重复
    symbol = Column(String(30), nullable=True,comment='代码 有可能有重复')
    # 市值
    market_cap = Column(String(100), nullable=True,comment='市值')
    # 价格
    price = Column(String(100), nullable=True,comment='价格')
    # 流通数量
    circulating_supply = Column(String(100), nullable=True,comment='流通数量')
    # 24小时成交量
    volume_24h = Column(String(100),nullable=True,comment='24小时成交量')
    # 一小时涨跌幅
    change_percent_1h = Column(String(30), nullable=True,comment='一小时涨跌幅')
    # % 24h涨跌幅
    change_percent_24h = Column(String(30), nullable=True,comment='% 24h涨跌幅')
    # % 7d涨跌幅
    change_percent_7d = Column(String(30), nullable=True,comment='% 7d涨跌幅')


    def __init__(self,dic):
        self.__dict__.update(dic)
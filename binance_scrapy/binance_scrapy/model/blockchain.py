#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 下午5:30
# @Author  : zhujinghui 
# @site    : 
# @File    : blockchain.py
# @Software: PyCharm

from sqlalchemy import Column,String,Integer,DateTime,Boolean

from . import Base
import datetime
class BlockChain(Base):
    __tablename__ = 'block_chain'

    # 英文名
    ename = Column(String(50),primary_key=True,nullable=True)
    # 代码 有可能有重复
    symbol = Column(String(30),nullable=False)
    # 市值
    market_cap = Column(String(100),nullable=True)
    # 发行总量
    max_supply = Column(String(100),nullable=True)
    # 流通数量
    circulating_supply = Column(String(100),nullable=True)
    # 发行价格
    issue_price = Column(String(100),nullable=True)
    # 发行日期
    issue_date = Column(String(20),nullable=True)
    # 官网
    website = Column(String(100),nullable=True)
    # 区块链浏览器
    explorer = Column(String(100),nullable=True)
    # 白皮书 英文
    white_paper_en = Column(String(100),nullable=True)
    # 白皮书 英文 状态
    white_paper_en_state = Column(Boolean, default=False)
    # 白皮书 中文
    white_paper_cn = Column(String(100),nullable=True)
    # 白皮书 中文 状态
    white_paper_cn_state = Column(Boolean, default=False)
    # 介绍 英文
    introduction_en = Column(String(5000),nullable=True)
    # 介绍 中文
    introduction_cn = Column(String(5000),nullable=True)
    # 媒体号
    social = Column(String(500),nullable=True)
    # 英文的url
    en_url = Column(String(100),nullable=True)
    # 中文的url
    cn_url = Column(String(100),nullable=True)

    def __init__(self,dic):
        self.__dict__.update(dic)



    # def __init__(self,symbol=None,ename=None,market_cap=None,max_supply=None,circulating_supply=None,issue_price=None,issue_date=None,website=None,explorer=None,white_paper_en=None,white_paper_cn=None,introduction_en=None,introduction_cn=None,social=None,en_url=None,cn_url=None):
    #     # 代码
    #     self.symbol = symbol
    #     # 英文名
    #     self.ename = ename
    #     # 市值
    #     self.market_cap = market_cap
    #     # 发行总量
    #     self.max_supply = max_supply
    #     # 流通数量
    #     self.circulating_supply = circulating_supply
    #     # 发行价格
    #     self.issue_price = issue_price
    #     # 发行日期
    #     self.issue_date = issue_date
    #     # 官网
    #     self.website = website
    #     # 区块链浏览器
    #     self.explorer = explorer
    #     # 白皮书 英文
    #     self.white_paper_en = white_paper_en
    #     # 白皮书 中文
    #     self.white_paper_cn = white_paper_cn
    #     # 介绍 英文
    #     self.introduction_en = introduction_en
    #     # 介绍 中文
    #     self.introduction_cn = introduction_cn
    #     # 媒体号
    #     self.social = social
    #     # 英文的url
    #     self.en_url = en_url
    #     # 中文的url
    #     self.cn_url = cn_url
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 下午5:27
# @Author  : zhujinghui 
# @site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:toor@localhost/binance?charset=utf8')


#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
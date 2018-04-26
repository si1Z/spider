#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 下午1:49
# @Author  : zhujinghui 
# @site    : 
# @File    : myhref_model.py
# @Software: PyCharm

from sqlalchemy import Column,String,Integer,DateTime,Boolean
from . import Base

class MyHrefModel(Base):
    __tablename__ = 'myhref'

    # 序号
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=True)
    # 代码
    code = Column(String(100), nullable=True)
    # 提交次数（近一个月）
    commitCountAMonth = Column(String(100), nullable=True)
    # 提交次数（上周）
    commitCountLastWeek = Column(String(100), nullable=True)
    # 提交次数（本周）
    commitCountAWeek = Column(String(100), nullable=True)
    # 代码量（近一个月
    addCodesCountAMonth = Column(String(100), nullable=True)
    # 代码量（上周
    addCodesCountLastWeek = Column(String(100), nullable=True)
    # 代码量（本周
    addCodesCountAWeek = Column(String(100), nullable=True)
    # 分支数
    forksCount = Column(String(100), nullable=True)
    # 问题数
    openIssuesCount = Column(String(100), nullable=True)
    # 订阅数
    subscribersCount = Column(String(100), nullable=True)
    # 关注数
    watchersCount = Column(String(100), nullable=True)
    # 项目库
    repo = Column(String(100), nullable=True)
    # 编程语言
    language = Column(String(100), nullable=True)
    # 创建
    createTime = Column(String(100), nullable=True)
    # 提交
    pushTime = Column(String(100), nullable=True)


    def __init__(self,dic):
        self.__dict__.update(dic)
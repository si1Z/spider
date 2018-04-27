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

    # html.push("<a target='_blank' href='https://github.com/" + info.owner + "'>" + info.code + "</a></td>");

    # 序号
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=True)
    # 代码
    code = Column(String(100), nullable=True,comment='序号')
    # github项目地址
    github_href = Column(String(300), nullable=True,comment='github项目地址')
    # 提交次数（近一个月）
    commitCountAMonth = Column(String(100), nullable=True,comment='提交次数（近一个月）')
    # 提交次数（上周）
    commitCountLastWeek = Column(String(100), nullable=True,comment='提交次数（上周）')
    # 提交次数（本周）
    commitCountAWeek = Column(String(100), nullable=True,comment='提交次数（本周）')
    # 代码量（近一个月)
    addCodesCountAMonth = Column(String(100), nullable=True,comment='代码量（近一个月)')
    # 代码量（上周)
    addCodesCountLastWeek = Column(String(100), nullable=True,comment='代码量（上周)')
    # 代码量（本周
    addCodesCountAWeek = Column(String(100), nullable=True,comment='代码量（本周')
    # 分支数
    forksCount = Column(String(100), nullable=True,comment='分支数')
    # 问题数
    openIssuesCount = Column(String(100), nullable=True,comment='问题数')
    # 订阅数
    subscribersCount = Column(String(100), nullable=True,comment='订阅数')
    # 关注数
    watchersCount = Column(String(100), nullable=True,comment='关注数')
    # 项目库
    repo = Column(String(100), nullable=True,comment='项目库')
    # 编程语言
    language = Column(String(100), nullable=True,comment='编程语言')
    # 创建
    createTime = Column(String(100), nullable=True,comment='创建')
    # 提交
    pushTime = Column(String(100), nullable=True,comment='提交')


    def __init__(self,dic):
        self.__dict__.update(dic)
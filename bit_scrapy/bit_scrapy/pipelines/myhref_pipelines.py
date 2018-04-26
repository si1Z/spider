#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 下午1:54
# @Author  : zhujinghui 
# @site    : 
# @File    : myhref_pipelines.py
# @Software: PyCharm

from ..model import Base,engine,loadSession
from ..model.myhref_model import MyHrefModel

class MyHrefPipeline(object):
    #搜索Base的所有子类，并在数据库中生成表
    Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        item_dict = dict(item)
        a = MyHrefModel(item_dict)
        session = loadSession()
        session.add(a)
        session.commit()
        return item

        # query1 = session.query(BlockChain)
        # query1.filter(BlockChain.ename == item_dict['ename']).update({BlockChain.max_supply: item_dict['max_supply'],BlockChain.circulating_supply: item_dict['circulating_supply']})
        # session.commit()

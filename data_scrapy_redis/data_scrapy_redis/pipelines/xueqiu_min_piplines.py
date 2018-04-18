#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 9:40
# @Author  : zhujinghui
# @File    : xueqiuminpiplines.py
# @Software: PyCharm
import redis

class XueQiuMinRedisStorePipeline(object):
    def __init__(self):
	    self.client = redis.Redis(host='47.94.19.25', password='root_db', port=6379, db=6)

    # pipeline默认调用
    def process_item(self, mink, spider):
        symbol = mink['symbol']
        print(symbol)
        # self.client.hset('min0', symbol, mink['datelist'])
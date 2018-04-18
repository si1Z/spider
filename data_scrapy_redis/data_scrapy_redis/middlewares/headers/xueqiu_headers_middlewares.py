#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/17 9:58
# @Author  : zhujinghui
# @File    : xueqiu_headers_middlewares.py
# @Software: PyCharm
import random
from ...utils.header import agents

class UserAgentMiddleware(object):
    """ CHANGE USER-AGENT """
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
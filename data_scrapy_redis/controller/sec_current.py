#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 10:48
# @Author  : zhujinghui
# @File    : sec_current.py
# @Software: PyCharm
import os
import time
while True:
    command = "scrapy crawl sec_current"
    os.system(command)
    time.sleep(3600)
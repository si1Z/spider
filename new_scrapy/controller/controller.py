#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/20 10:26
# @Author  : zhujinghui
# @File    : controller.py
# @Software: PyCharm
import os
import time
# #获取当前工作目录
# print(os.getcwd())
#更改当前工作目录
# os.chdir('../')
# print(os.getcwd())
while True:
    a = os.system("scrapy crawl tx_news_update2")
    time.sleep(1800)

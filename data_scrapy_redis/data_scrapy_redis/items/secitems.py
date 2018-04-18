#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 17:06
# @Author  : zhujinghui
# @File    : secitems.py
# @Software: PyCharm
import scrapy

class SecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #公司
    company = scrapy.Field()
    #公司url
    company_url = scrapy.Field()

    form = scrapy.Field()

    index = scrapy.Field()
    index_url = scrapy.Field()
    #cik
    cik_num = scrapy.Field()
    accession_number = scrapy.Field()
    act = scrapy.Field()
    size = scrapy.Field()
    #接受时间
    accepted_time = scrapy.Field()
    filing_date = scrapy.Field()

    report_name = scrapy.Field()
    #公告url
    report_url = scrapy.Field()
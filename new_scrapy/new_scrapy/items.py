# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSimpleItem(scrapy.Item):
    #时间
    newsdate = scrapy.Field()
    # tmp
    tmp = scrapy.Field()
    # 内容摘录
    simpletext= scrapy.Field()
    # 网址
    newsurl = scrapy.Field()
    #股票号
    symbol = scrapy.Field()

class NewsArticleItem(scrapy.Item):
    #股票号
    symbol = scrapy.Field()
    #时间
    newsdate = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 内容
    body = scrapy.Field()
    #关键字
    keywords = scrapy.Field()
    # 网址
    newsurl = scrapy.Field()
    # 来源
    source = scrapy.Field()



class UsStockHomeItem(scrapy.Item):
    searchkey = scrapy.Field()
    tagname = scrapy.Field()
    # 股票号
    symbol = scrapy.Field()
    # 标题
    title = scrapy.Field()
    #内容
    body = scrapy.Field()

    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BinanceScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BlockChainItem(scrapy.Item):
    # define the fields for your item here like:
    #代码
    symbol = scrapy.Field()
    #英文名
    ename = scrapy.Field()
    #市值
    market_cap = scrapy.Field()
    #发行总量
    max_supply = scrapy.Field()
    #流通数量
    circulating_supply = scrapy.Field()
    #发行价格
    issue_price = scrapy.Field()
    #发行日期
    issue_date = scrapy.Field()
    #官网
    website = scrapy.Field()
    #区块链浏览器
    explorer = scrapy.Field()
    #白皮书 英文
    white_paper_en = scrapy.Field()
    # 白皮书 中文
    white_paper_cn = scrapy.Field()
    #介绍 英文
    introduction_en = scrapy.Field()
    # 介绍 中文
    introduction_cn = scrapy.Field()
    #媒体号
    social = scrapy.Field()
    #英文的url
    en_url = scrapy.Field()
    #中文的url
    cn_url = scrapy.Field()


if __name__ == "__main__":
    item = BinanceScrapyItem()
    item.keys()


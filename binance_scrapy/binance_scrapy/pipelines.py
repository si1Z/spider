# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .model import Base,engine,loadSession
from .model import blockchain


class BlockChainPipeline(object):
    #搜索Base的所有子类，并在数据库中生成表
    Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        a = blockchain.BlockChain(
            # 代码
            symbol= item['symbol'],
            # 英文名
            ename = item['ename'],
            # 市值
            # market_cap = item['market_cap'],
            # 发行总量
            # max_supply = item['max_supply'],
            # 流通数量
            # circulating_supply = item['circulating_supply'],
            # 发行价格
            issue_price = item['issue_price'],
            # 发行日期
            issue_date = item['issue_date'],
            # 官网
            website = item['website'],
            # 区块链浏览器
            explorer = item['explorer'],
            # 白皮书 英文
            white_paper_en = item['white_paper_en'],
            # 白皮书 中文
            white_paper_cn = item['white_paper_cn'],
            # 介绍 英文
            introduction_en = item['introduction_en'],
            # 介绍 中文
            introduction_cn = item['introduction_cn'],
            # 媒体号
            social = item['social'],
            # 英文的url
            en_url = item['en_url'],
            # 中文的url
            cn_url = item['cn_url'],
        )
        # a = blockchain.BlockChain(
        #     for key in item.keys():
        #         pass
        # )
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # print(a)
        session = loadSession()
        session.add(a)
        session.commit()
        # return item

class BinanceScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

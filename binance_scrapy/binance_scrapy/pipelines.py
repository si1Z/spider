# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from .model import Base,engine,loadSession
from .model import blockchain

from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join

import requests
import os

base_dir = "../../white_paper/"

def download(name,url):
    # filename = os.path.basename(url)
    extension = os.path.splitext(url)[1]
    filename = "{}{}".format(name,extension)
    proxies = {"https": "https://127.0.0.1:1087"}
    rsp = requests.get(url, proxies=proxies)
    rsp.raise_for_status()
    with open('{}{}'.format(base_dir,filename),'wb') as f:
        f.write(rsp.content)
    return (True,filename)

class MyFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url)


    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)),basename(path))

class BlockChainPipeline(object):
    #搜索Base的所有子类，并在数据库中生成表
    Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        # a = blockchain.BlockChain(
        #     # 代码
        #     symbol= item['symbol'],
        #     # 英文名
        #     ename = item['ename'],
        #     # 市值
        #     # market_cap = item['market_cap'],
        #     # 发行总量
        #     # max_supply = item['max_supply'],
        #     # 流通数量
        #     # circulating_supply = item['circulating_supply'],
        #     # 发行价格
        #     issue_price = item['issue_price'],
        #     # 发行日期
        #     issue_date = item['issue_date'],
        #     # 官网
        #     website = item['website'],
        #     # 区块链浏览器
        #     explorer = item['explorer'],
        #     # 白皮书 英文
        #     white_paper_en = item['white_paper_en'],
        #     # 白皮书 中文
        #     white_paper_cn = item['white_paper_cn'],
        #     # 介绍 英文
        #     introduction_en = item['introduction_en'],
        #     # 介绍 中文
        #     introduction_cn = item['introduction_cn'],
        #     # 媒体号
        #     social = item['social'],
        #     # 英文的url
        #     en_url = item['en_url'],
        #     # 中文的url
        #     cn_url = item['cn_url'],
        # )
        try:
            if 'white_paper_en' in item:
                e_url = item['white_paper_en']
                e_white_paper_name = "en_{}_{}".format(item['symbol'],item['ename'])
                e_state,e_name = download(e_white_paper_name,e_url)
                item['white_paper_en_state'] = e_state
            if 'white_paper_cn' in item:
                c_url = item['white_paper_cn']
                c_white_paper_name = "cn_{}_{}".format(item['symbol'],item['ename'])
                download(c_white_paper_name, c_url)
                c_state, c_name = download(c_white_paper_name, c_url)
                item['white_paper_cn_state'] = c_state
        except:
            print("xxxxxxxxxxxxxxxxxx")

        item_dict = dict(item)
        a = blockchain.BlockChain(item_dict)
        session = loadSession()
        session.add(a)
        session.commit()
        # return item


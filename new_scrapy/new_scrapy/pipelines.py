# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
from twisted.enterprise import adbapi
import json
import logging
import requests
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ServiceArticlePipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self.settings = settings
        # self.url = "https://www.xinbozhengquan.com/bussiness/news_service/add_news_stock2.json"
        self.url = "http://39.106.143.83:8070/bussiness/news_service/add_news_stock2.json"
    # pipeline默认调用
    def process_item(self, item, spider):
        def tran(item):
            data_dict = {"tagStock":[item['symbol']],
                       "title":item['title'],
                       "source":item['source'],
                       "content":item['body'],
                       "link":item['newsurl'],
                        "sourcetime":item['newsdate']
                       }
            datajsonstr = json.JSONEncoder().encode(data_dict)
            return datajsonstr

        rsp= requests.post(self.url, tran(item),timeout=0.1)
        resultjson=json.JSONDecoder().decode(rsp.text)
        print(resultjson)
        if resultjson['status'] == 'C_200':
            print("................成功..........................")
        else:
            print('有缺参数的......................')
            # with open('err2.txt','a',encoding='utf-8') as f:
            #     f.write('..............................\n'+str(resultjson)+'\n'+str(item)+'\n..............................')


class MySQLStoreArticlePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 字典转换为 字符串
    def dict_2_str(self, dictin):
        tmplist = []
        for k, v in dictin.items():
            tmp = '%s="%s"' % (str(k), str(v).replace('"', "'"))
            tmplist.append(' ' + tmp + ' ')
            strr = ','.join(tmplist)
        return strr
        # 获得插入语句

    def get_i_sql(self, table, dict):
        sql = 'insert into %s set ' % table
        sql += self.dict_2_str(dict)
        return sql

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        data_dict = dict(item)
        table = 'us_stocks_news'
        sql = self.get_i_sql(table,data_dict)
        conn.execute(sql)

    # 异常处理
    def _handle_error(self, failue, item, spider):
        logging.error('...............')

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url =  item['image_url']
        yield Request(image_url,meta={'item':item})

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        image_dir = item['searchkey']
        image_name = item['image_name']
        filePathAndName = '{0}/{1}'.format(image_dir, image_name)
        return filePathAndName

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_path'] = image_paths
        return item

class JsonPipeline(object):
    def __init__(self):
        self.basedir = "D:/data/json/"
    def process_item(self, item, spider):
        symbol = item['symbol']
        filePathAndName = self.basedir + str(symbol) + ".json"
        with open(filePathAndName, 'w', encoding='utf-8') as f:
            json.dump(dict(item),f,ensure_ascii=False)
        # return item
    def spider_closed(self, spider):
        print("成功................")

class MongoDBPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self,settings):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        # connection = pymongo.Connection(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return item
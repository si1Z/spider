# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql

from DBUtils.PooledDB import PooledDB
from scrapy.exceptions import DropItem

# 字典转换为字符串
def dict_2_str(dictin):
    tmplist = []
    for k, v in dictin.items():
        tmp = '`%s`="%s"' % (str(k), str(v).replace('"', "'"))
        tmplist.append(' ' + tmp + ' ')
        strr = ','.join(tmplist)
    return strr
# 获得插入语句
def get_i_sql(table, dict):
    sql = 'insert into %s set ' % table
    sql += dict_2_str(dict)
    return sql

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

class MySQLDBPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        self.pool = PooledDB(pymysql,5,**dbargs)  # 5为连接池里的最少连接数
        self.table = settings['MYSQL_TABLE']

    def open_spider(self, spider):
        pass

    # pipeline默认调用
    def process_item(self, item, spider):
        self._do_upinsert(item,spider)

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.pool.close()
    # 将每行更新或写入数据库中
    def _do_upinsert(self,item, spider):
        conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cur = conn.cursor()

        data_dict = dict(item)
        table = self.table
        sql = get_i_sql(table, data_dict)
        print(sql)
        cur.execute(sql)
        conn.commit()


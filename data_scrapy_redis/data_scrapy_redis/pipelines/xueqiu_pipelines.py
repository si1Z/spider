#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/12 16:55
# @Author  : zhujinghui
# @File    : xueqiupiplines.py
# @Software: PyCharm
import redis
import pymysql
from DBUtils.PooledDB import PooledDB
from ..items.xueqiuitems import SnapshotItem ,BaseItem

# 字典转换为字符串
def dict_2_str(dictin):
    tmplist = []
    for k, v in dictin.items():
        tmp = '%s="%s"' % (str(k), str(v).replace('"', "'"))
        tmplist.append(' ' + tmp + ' ')
        strr = ','.join(tmplist)
    return strr
# 获得插入语句
def get_i_sql(table, dict):
    sql = 'insert into %s set ' % table
    sql += dict_2_str(dict)
    return sql

class XueQiuRedisStorePipeline(object):
    def __init__(self):
        self.client = redis.Redis(host='47.94.19.25', password='root_db', port=6379, db=6)

    def process_item(self, item, spider):
        if isinstance(item, SnapshotItem):
            data_dict = dict(item)
            self.client.set(data_dict['CODE'], data_dict)
            return item
        elif isinstance(item, BaseItem):
            basedata_dict = dict(item)
            self.client.set('base_data:'+ str(basedata_dict['symbol']),basedata_dict)
            return item

class MySQLStorePipeline_sec(object):
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
        if isinstance(item, SnapshotItem):
            try:
                self._do_upinsert(item, spider)
            except:
                pass
            return item
        elif isinstance(item, BaseItem):
            pass

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()

    # 将每行更新或写入数据库中
    def _do_upinsert(self,item, spider):
        conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cur = conn.cursor()

        data_dict = dict(item)
        table = self.table
        sql = get_i_sql(table, data_dict)

        cur.execute(sql)
        conn.commit()







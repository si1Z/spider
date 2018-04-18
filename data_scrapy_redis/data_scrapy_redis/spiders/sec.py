# -*- coding: utf-8 -*-
import scrapy
import time
import re
import sys
import pymysql
from ..items.secitems import SecItem
from bs4 import BeautifulSoup
from scrapy.http import Request
from urllib.parse import parse_qs,urlparse
from datetime import date,timedelta,datetime

#........... 正式服
# 'MYSQL_HOST': 'rm-2zebj0vhwd2f6vy4w.mysql.rds.aliyuncs.com',
# 'MYSQL_DBNAME': 'xhyg_us_stocks',
# 'MYSQL_USER': 'yigukeji_db',
# 'MYSQL_PASSWD': 'Yigukeji_dba',
# 'MYSQL_TABLE': 'us_reports',


#................测试服
MYSQL_HOST = '39.106.159.159'
MYSQL_DBNAME = 'xhyg_us_stocks'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'ygkjtest'
MYSQL_TABLE = 'us_reports'




# current  监测有新公告时立刻 更新
def get_last_data():
    # 'MYSQL_TABLE': 'us_reports',
    try:
        conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME, charset='utf8')
        sql = "SELECT accepted_time,cik_num FROM us_reports ORDEr by accepted_time DESC,cik_num DESC LIMIT 0,100"
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result[0]
    except:
        print("xxxxxxxxxxxxx")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
head_url = "https://www.sec.gov"
class SecCurrentSpider(scrapy.Spider):
    name = "sec_current"
    allowed_domains = ["www.sec.gov"]
    start_urls = ['https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent']
    custom_settings = {
        'DUPEFILTER_CLASS':None,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        },

        'MYSQL_HOST': MYSQL_HOST,
        'MYSQL_DBNAME': MYSQL_DBNAME,
        'MYSQL_USER': MYSQL_USER,
        'MYSQL_PASSWD': MYSQL_PASSWD,
        'MYSQL_TABLE': MYSQL_TABLE,

        'ITEM_PIPELINES': {
            # 'sec_scrapy.pipelines.MongoDBPipeline': 100,
            'data_scrapy_redis.pipelines.sec_pipelines.MySQLDBPipeline': 200,
        },
    }
    def __init__(self):
        self.lastdata = get_last_data()
        self.lasttime = self.lastdata[0]
        self.lastcik = self.lastdata[1]
        print(".............................................")
        print(self.lasttime)
    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        # soup = BeautifulSoup(response.body, 'lxml')
        div = soup.find('div', style="margin-left: 10px")

        tables = div.find_all('table', summary='', recursive=False)
        trs = tables[1].find_all('tr', recursive=False)
        del trs[0]
        num = len(trs)
        for i in range(0, num, 2):
            item = SecItem()

            a_tag = trs[i].find_all('td', recursive=False)[2].a
            item['company'] = a_tag.text.strip()
            item['company_url'] = head_url + a_tag['href'].strip()

            url_params = urlparse(item['company_url'])
            item['cik_num'] = ','.join(parse_qs(url_params.query)['CIK'])
#.........................................................................
            index_tds = trs[i+1].find_all('td', recursive=False)

            item['form'] = index_tds[0].text.strip()

            item['index_url'] = head_url + index_tds[1].find_all('a', recursive=False)[0]['href'].strip()
            item['index'] = index_tds[2].get_text('\n').replace('\xa0', ' ').strip()
            tmp = item['index'].split('\n')[-1]
            tmp_prams_list = tmp.split(': ')
            item['accession_number'] = tmp_prams_list[1].split(' ')[0].strip()
            if len(tmp_prams_list) == 4:
                item['act'] = tmp_prams_list[2].split(' ')[0].strip()

            item['size'] = tmp_prams_list[-1].strip()

            accepted_text = index_tds[3].text.strip()
            item['accepted_time'] = accepted_text[:10]+" "+accepted_text[10:]

            item['filing_date'] = int(time.mktime(time.strptime(index_tds[4].text.strip(), "%Y-%m-%d"))*1000)

            if item['accepted_time'] == self.lasttime and item['cik_num'] == self.lastcik:
                sys.exit(0)
            yield Request(item['index_url'], meta={'item': item}, callback=self.parse_document)

        forms = div.find_all('form', recursive=False)
        input_tags = forms[0].find_all('input', recursive=False)
        input_url = input_tags[-1]['onclick'].replace('parent.location=', '').replace("'", '')
        next40_url = head_url + input_url
        yield Request(next40_url,callback=self.parse,dont_filter=True)

    def parse_document(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        item = response.meta['item']

        table = soup.find('table', class_="tableFile", summary="Document Format Files")
        trs = table.find_all('tr', recursive=False)
        del trs[0]
        tmp_names = []
        tmp_urls = []
        for tr in trs:
            a_tag = tr.find_all('td', recursive=False)[2].a
            if a_tag.text.strip().endswith('.htm') or a_tag.text.strip().endswith('.html'):
                head_url = "https://www.sec.gov"
                url = head_url + a_tag['href'].strip()
                tmp_urls.append(url)

                tmp_names.append(a_tag.text.strip())
        if tmp_urls:
            item['report_url'] = ','.join(tmp_urls)
            item['report_name'] = ','.join(tmp_names)

        yield item


# 指定 时间段 抓取公告
def get_urls():
    # beginDate = date(2016, 1, 1)
    # endDate = date(2017, 10, 13)
    beginDate = date(2017, 10, 14)
    endDate = date(2017, 12, 4)
    aDay = timedelta(days=1)
    baseUrl = "https://www.sec.gov/cgi-bin/srch-edgar?text=FILING-DATE%3D{}&first=2016&last=2017"

    while True:
        beginDate = beginDate + aDay

        dataStr = beginDate.strftime('%Y%m%d')
        yield baseUrl.format(dataStr)
        if beginDate == endDate:
            break
class SecAllSpider(scrapy.Spider):
    name = "sec_all"
    allowed_domains = ["www.sec.gov"]
    # start_urls = ['https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent']
    start_urls = get_urls()

    def __init__(self, category=None, *args, **kwargs):
        super(SecAllSpider, self).__init__(*args, **kwargs)
        # self.start_urls = ['http://www.baidu.com']
        # self.datetime = "abcde"

    custom_settings = {

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        },

        # 'MONGODB_SERVER':'10.9.210.109',
        # 'MONGODB_PORT':27017,
        # 'MONGODB_DB':'sec_database',
        # 'MONGODB_COLLECTION':'reports',

        'MYSQL_HOST': MYSQL_HOST,
        'MYSQL_DBNAME': MYSQL_DBNAME,
        'MYSQL_USER': MYSQL_USER,
        'MYSQL_PASSWD': MYSQL_PASSWD,
        'MYSQL_TABLE': MYSQL_TABLE,

        'ITEM_PIPELINES': {
            # 'data_scrapy_redis.pipelines.sec_pipelines.MongoDBPipeline': 100,
            'data_scrapy_redis.pipelines.sec_pipelines.MySQLDBPipeline': 200,
        },
    }

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        # soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find_all('table')[4]
        trs = table.find_all('tr')
        del trs[0]
        head_url = "https://www.sec.gov"
        for tr in trs:
            item = SecItem()
            tds = tr.find_all('td', recursive=False)
            company_a = tds[1].a
            item['company'] = company_a.text.strip()
            item['company_url'] = head_url + company_a.get('href').strip()
            item['index_url'] = head_url + tds[2].find_all('a', recursive=False)[-1].get('href')
            # item['index'] =
            item['form'] = tds[3].text.strip()
            item['size'] = str(round(int(tds[5].text.strip())/1000,2))+'k'
            yield Request(item['index_url'], meta={'item': item}, callback=self.parse_document)

        last_a_tag = soup.find_all('center')[-1].find_all('a',recursive=False)[-1]
        a_text = last_a_tag.text.strip()
        if a_text =='[NEXT]':
            nexturl = "https://www.sec.gov"+last_a_tag.get('href')
            yield Request(nexturl,callback=self.parse)

    def parse_document(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        item = response.meta['item']

        div = soup.find('div', id='contentDiv')
        divs = div.find_all('div', recursive=False)
        # ............
        headbody = divs[0].find_all('div', recursive=False)
        item['accession_number'] = headbody[0].find('div', id='secNum').contents[2].strip()

        tmp = headbody[1].find_all('div', class_='formGrouping', recursive=False)[0]
        item['accepted_time'] = tmp.find('div', text='Accepted').find_next().text
        # ...................................
        table = divs[1].find('table', class_="tableFile", summary="Document Format Files")
        trs = table.find_all('tr', recursive=False)
        del trs[0]
        tmp_names = []
        tmp_urls = []
        for tr in trs:
            a_tag = tr.find_all('td', recursive=False)[2].a
            if a_tag.text.strip().endswith('.htm') or a_tag.text.strip().endswith('.html'):
                head_url = "https://www.sec.gov"
                url = head_url + a_tag['href'].strip()
                tmp_urls.append(url)

                tmp_names.append(a_tag.text.strip())
        if tmp_urls:
            item['report_url'] = ','.join(tmp_urls)
            item['report_name'] = ','.join(tmp_names)
        # .......................
        companyInfo = divs[-1].find('div', class_="companyInfo")
        cik = companyInfo.find('a', href=re.compile('.*?CIK=.*?action=getcompany')).text.replace(" (see all company filings)",'')
        item['cik_num'] = cik
        try:
            item['act'] = companyInfo.find('p', class_="identInfo").contents[3].text
        except:
            print("..............................")

        if item['report_url'] !='':
            yield item
            # print(item)


# 将公告更新到昨天
def get_last_datetime():
    # 'MYSQL_TABLE': 'us_reports',
    try:
        conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME, charset='utf8')
        sql = "SELECT accepted_time FROM us_reports ORDEr by accepted_time DESC LIMIT 0,100"
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]
    except:
        print("xxxxxxxxxxxxx")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
def get_update_urls():
    # beginDate = date(2016, 1, 1)
    # endDate = date(2017, 10, 13)
    tmp = get_last_datetime()
    dtime = datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S')
    aDay = timedelta(days=1)
    beginDate = dtime.date() + aDay

    now = datetime.now().date()
    endDate = now - aDay

    baseUrl = "https://www.sec.gov/cgi-bin/srch-edgar?text=FILING-DATE%3D{}&first=2016&last=2017"

    while True:
        beginDate = beginDate + aDay

        dataStr = beginDate.strftime('%Y%m%d')
        yield baseUrl.format(dataStr)
        if beginDate == endDate:
            break
class SecUpdateSpider(scrapy.Spider):
    name = "sec_update"
    allowed_domains = ["www.sec.gov"]
    # start_urls = ['https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent']
    start_urls = get_update_urls()

    custom_settings = {

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
        },
        'MYSQL_HOST': MYSQL_HOST,
        'MYSQL_DBNAME': MYSQL_DBNAME,
        'MYSQL_USER': MYSQL_USER,
        'MYSQL_PASSWD': MYSQL_PASSWD,
        'MYSQL_TABLE': MYSQL_TABLE,

        'ITEM_PIPELINES': {
            # 'data_scrapy_redis.pipelines.sec_pipelines.MongoDBPipeline': 100,
            'data_scrapy_redis.pipelines.sec_pipelines.MySQLDBPipeline': 200,
        },
    }

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        # soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find_all('table')[4]
        trs = table.find_all('tr')
        del trs[0]
        head_url = "https://www.sec.gov"
        for tr in trs:
            item = SecItem()
            tds = tr.find_all('td', recursive=False)
            company_a = tds[1].a
            item['company'] = company_a.text.strip()
            item['company_url'] = head_url + company_a.get('href').strip()
            item['index_url'] = head_url + tds[2].find_all('a', recursive=False)[-1].get('href')
            # item['index'] =
            item['form'] = tds[3].text.strip()
            item['size'] = str(round(int(tds[5].text.strip())/1000,2))+'k'
            yield Request(item['index_url'], meta={'item': item}, callback=self.parse_document)

        last_a_tag = soup.find_all('center')[-1].find_all('a',recursive=False)[-1]
        a_text = last_a_tag.text.strip()
        if a_text =='[NEXT]':
            nexturl = "https://www.sec.gov"+last_a_tag.get('href')
            yield Request(nexturl,callback=self.parse)

    def parse_document(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        item = response.meta['item']

        div = soup.find('div', id='contentDiv')
        divs = div.find_all('div', recursive=False)
        # ............
        headbody = divs[0].find_all('div', recursive=False)
        item['accession_number'] = headbody[0].find('div', id='secNum').contents[2].strip()

        tmp = headbody[1].find_all('div', class_='formGrouping', recursive=False)[0]
        item['accepted_time'] = tmp.find('div', text='Accepted').find_next().text
        # ...................................
        table = divs[1].find('table', class_="tableFile", summary="Document Format Files")
        trs = table.find_all('tr', recursive=False)
        del trs[0]
        tmp_names = []
        tmp_urls = []
        for tr in trs:
            a_tag = tr.find_all('td', recursive=False)[2].a
            if a_tag.text.strip().endswith('.htm') or a_tag.text.strip().endswith('.html'):
                head_url = "https://www.sec.gov"
                url = head_url + a_tag['href'].strip()
                tmp_urls.append(url)

                tmp_names.append(a_tag.text.strip())
        if tmp_urls:
            item['report_url'] = ','.join(tmp_urls)
            item['report_name'] = ','.join(tmp_names)
        # .......................
        companyInfo = divs[-1].find('div', class_="companyInfo")
        cik = companyInfo.find('a', href=re.compile('.*?CIK=.*?action=getcompany')).text.replace(" (see all company filings)",'')
        item['cik_num'] = cik
        try:
            item['act'] = companyInfo.find('p', class_="identInfo").contents[3].text
        except:
            print("..............................")

        if item['report_url'] !='':
            yield item
            # print(item)

# -*- coding: utf-8 -*-
import scrapy
from ..items import BlockChainItem
from scrapy.http import Request
from bs4 import BeautifulSoup

class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['binance.com']
    # start_urls = ["https://info.binance.com/en/","https://info.binance.com/cn/"]
    start_urls = ["https://info.binance.com/en/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
            'binance_scrapy.middlewares.ProxyMiddleware': 100,
        },

        'ITEM_PIPELINES': {
            'binance_scrapy.pipelines.BlockChainPipeline': 100,
        },
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        body = soup.find('tbody')
        trs = body.find_all('tr', recursive=False)

        base_url = 'https://info.binance.com{}'
        for tr in trs:
            url = base_url.format(tr.get('link'))
            item = BlockChainItem()
            yield Request(url, meta={'item': item},callback=self.parse_document_en, dont_filter=True)

    def parse_document_en(self, response):
        en_url = response.url
        cn_url = en_url.replace('/en/','/cn/')
        item = response.meta['item']

        item['en_url'] = en_url
        item['cn_url'] = cn_url

        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')

        div = soup.find('div', class_='content-box')

        # 上边
        content_top = div.find('div', class_='row content-top')
        # 。。。。左边
        h4 = content_top.find('h4', class_='media-heading')
        symbol = h4.font.text    #.................................
        ename = h4.span.text.replace('(', "").replace(')', "")  #.............................

        if symbol:
            item['symbol'] = symbol
        if ename:
            item['ename'] = ename

        # 。。。。右边
        maket_info = content_top.find('div', class_='row maket-info')
        divs = maket_info.find_all('div', recursive=False)
        for tmp in divs:
            if str(tmp.span.text).startswith('Market Cap'):
                pass
            if str(tmp.span.text).startswith('Max Supply'):
                pass
            if str(tmp.span.text).startswith('Circulating Supply'):
                pass
            if str(tmp.span.text).startswith('Issue Price'):
                try:
                    symb = tmp.find('strong', class_='symbol').text
                    num = tmp.find('font', class_='symbolNum three').text #.....................
                    issue_price = "{}{}".format(symb, num)
                except:
                    issue_price = None
                if issue_price:
                    item['issue_price'] = issue_price
            if str(tmp.span.text).startswith('Issue Date'):
                issue_date = tmp.find('strong').text        #............................
                if issue_date:
                    item['issue_date'] = issue_date

        # 左边
        ul_left = div.find('ul', class_='pull-left')
        lis_left = ul_left.find_all('li')
        for li_left in lis_left:
            if str(li_left.text).startswith("Website"):
                website = li_left.a.get('href')  # ................
                if website:
                    item['website'] = website
            if str(li_left.text).startswith("Explorer"):
                explorer = li_left.a.get('href')  # ................
                if explorer:
                    item['explorer'] = explorer
            if str(li_left.text).startswith("White Paper"):
                white_paper_en = li_left.a.get('href')  # ................
                if white_paper_en:
                    item['white_paper_en'] = white_paper_en

        # 右边
        social = {}
        ul_right = div.find('ul', class_='pull-right')
        if ul_right != None:
            lis_right = ul_right.find_all('li')
            del lis_right[0]
            for li_right in lis_right:
                social[li_right.a.get('title')] = li_right.a.get('href') #...............

        if social:
            item['social'] = social

        # 介绍
        content_text = div.find('div', class_='content-text')
        if content_text:
            content_text_con = content_text.find('div', class_='content-text-con')
            ps = content_text_con.find_all('p')
            introduction_list = []
            for p in ps:
                introduction_list.append(p.text)
                introduction_en = '\n'.join(introduction_list)  #.............................

            if introduction_en:
                item['introduction_en'] = introduction_en

        yield Request(cn_url, meta={'item': item}, callback=self.parse_document_cn, dont_filter=True)

    def parse_document_cn(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')

        div = soup.find('div', class_='content-box')

        # # 上边
        # content_top = div.find('div', class_='row content-top')
        # # 。。。。左边
        # h4 = content_top.find('h4', class_='media-heading')
        # symbol = h4.font.text    #.................................
        # ename = h4.span.text.replace('(', "").replace(')', "")  #.............................
        #
        # if symbol:
        #     item['symbol'] = symbol
        # if ename:
        #     item['ename'] = ename

        # # 。。。。右边
        # maket_info = content_top.find('div', class_='row maket-info')
        # divs = maket_info.find_all('div', recursive=False)
        # for tmp in divs:
        #     if str(tmp.span.text).startswith('Market Cap'):
        #         pass
        #     if str(tmp.span.text).startswith('Max Supply'):
        #         pass
        #     if str(tmp.span.text).startswith('Circulating Supply'):
        #         pass
        #     if str(tmp.span.text).startswith('Issue Price'):
        #         try:
        #             symb = tmp.find('strong', class_='symbol').text
        #             num = tmp.find('font', class_='symbolNum three').text #.....................
        #             issue_price = "{}{}".format(symb, num)
        #         except:
        #             issue_price = None
        #         if issue_price:
        #             item['issue_price'] = issue_price
        #     if str(tmp.span.text).startswith('Issue Date'):
        #         issue_date = tmp.find('strong').text        #............................
        #         if issue_date:
        #             item['issue_date'] = issue_date






        # 左边
        ul_left = div.find('ul', class_='pull-left')
        lis_left = ul_left.find_all('li')
        for li_left in lis_left:
            # if str(li_left.text).startswith("Website"):
            #     website = li_left.a.get('href')  # ................
            #     if website:
            #         item['website'] = website
            # if str(li_left.text).startswith("Explorer"):
            #     explorer = li_left.a.get('href')  # ................
            #     if explorer:
            #         item['explorer'] = explorer
            if str(li_left.text).startswith("白皮书"):
                white_paper_cn = li_left.a.get('href')  # ................
                if white_paper_cn:
                    item['white_paper_cn'] = white_paper_cn

        # # 右边
        # social = {}
        # ul_right = div.find('ul', class_='pull-right')
        # if ul_right != None:
        #     lis_right = ul_right.find_all('li')
        #     del lis_right[0]
        #     for li_right in lis_right:
        #         social[li_right.a.get('title')] = li_right.a.get('href') #...............
        #
        # if social:
        #     item['social'] = social

        # 介绍
        content_text = div.find('div', class_='content-text')
        if content_text:
            content_text_con = content_text.find('div', class_='content-text-con')
            ps = content_text_con.find_all('p')
            introduction_list = []
            for p in ps:
                introduction_list.append(p.text)
                introduction_cn = '\n'.join(introduction_list)  #.............................

            if introduction_cn:
                item['introduction_cn'] = introduction_cn

        print(item)

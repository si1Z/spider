# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from ..items import UsStockHomeItem

class Usstock21homeSpider(scrapy.Spider):
    name = "home21"
    allowed_domains = ["www.mg21.com"]
    start_urls = ['http://www.mg21.com/']
    # start_urls = ['http://www.mg21.com/ikea.html']
    custom_settings = {
        'IMAGES_STORE' : 'D:/data/img',  # 图片存储路径
        'IMAGES_EXPIRES' : 90 , # 过期天数
        'IMAGES_MIN_HEIGHT' : 3,  # 图片的最小高度
        'IMAGES_MIN_WIDTH' : 3 , # 图片的最小宽度
        # 图片的尺寸小于IMAGES_MIN_WIDTH*IMAGES_MIN_HEIGHT的图片都会被过滤

        'ITEM_PIPELINES': {
            'new_scrapy.pipelines.MyImagesPipeline': 100,
            'new_scrapy.pipelines.JsonPipeline': 200,
        },
    }

    # def parse(self,response):
    #     soup = BeautifulSoup(response.body_as_unicode(),'lxml')
    #     item = UsStockHomeItem()
    #     item['symbol'] = str(response.url).split("/")[-1].split(".")[0].upper()
    #     item['title'] = soup.find('h1',class_="entry-title").text
    #
    #     textparts = soup.find('div', class_="single-content")
    #     texttag = textparts.find_all(['p', 'ul', 'h2', 'h3'], recursive=False)
    #     imgurl = str()
    #     body = str()
    #     for line in texttag:
    #         try:
    #             imgnode = line.findChild("img")
    #             if imgnode:
    #                 imgurl = imgnode['data-original']
    #             body = body + str(line.text)
    #         except:
    #             pass
    #     item['image_url'] = imgurl
    #     item['body'] = body
    #     return item

    def parse(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        tagdiv = soup.find('div', class_="tagcloud")
        ahrefs = tagdiv.findAll('a')
        for a in ahrefs:
            searchkey = str(a.text).strip()
            url = str(a['href']).strip()

            yield Request(url, meta={'searchkey':searchkey}, callback=self.parse_page)

    def parse_page(self,response):
        searchkey = response.meta["searchkey"]
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        articles = soup.findAll('article', attrs={'data-wow-delay': "0.3s"})
        for article in articles:
            tagname = article.find('span', class_="cat").text
            url = article.a['href']
            yield Request(url, meta={'searchkey': searchkey,'tagname':tagname}, callback=self.parse_text)

        nav_div = soup.find('div', class_="nav-links")
        nextpage = nav_div.find('a', class_="next page-numbers")
        if nextpage:
            url = nextpage['href']
            yield Request(url, meta={'searchkey': searchkey}, callback=self.parse_page)

    def parse_text(self,response):
        soup = BeautifulSoup(response.body_as_unicode(),'lxml')
        item = UsStockHomeItem()
        item['searchkey'] = response.meta['searchkey']
        item['tagname'] = response.meta['tagname']
        item['symbol'] = str(response.url).split("/")[-1].split(".")[0].upper()
        item['title'] = soup.find('h1',class_="entry-title").text

        textparts = soup.find('div', class_="single-content")
        texttag = textparts.find_all(['p', 'ul', 'h2', 'h3'], recursive=False)
        imgurl = str()
        body = str()
        for line in texttag:
            try:
                imgnode = line.findChild("img")
                if imgnode:
                    imgurl = imgnode['data-original']
                body = body + str(line.text)
            except:
                pass
        item['image_url'] = imgurl
        item['image_name'] = imgurl.split('/')[-1]
        item['body'] = body
        return item
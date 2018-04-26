#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 下午6:15
# @Author  : zhujinghui 
# @site    : 
# @File    : tt.py
# @Software: PyCharm
import requests
from scrapy.http import HtmlResponse

# url = "https://coinmarketcap.com/all/views/all/"
#
# rsp = requests.get(url)
#
# with open('a.txt','w') as f:
#     f.write(rsp.text)

with open('a.txt','r') as f:
    text = f.read()

response = HtmlResponse(url='http://www.test.com',body=text,encoding='utf-8')

# response.body_as_unicode()

table = response.xpath('//table[@id="currencies-all"]')[0]
# print(table)

header = table.xpath('./thead//tr')[0]
# header
ths = header.xpath('./th/text()')

#
# for th in ths:
#     print(th.extract().strip(),end='\t')

# print(header)

from bit_scrapy.bit_scrapy.items import CoinItem


trs = table.xpath('./tbody//tr')



tr = trs[0]
tds= tr.xpath('./td')
print(tds[0].extract())

# for tr in trs:
#     tds= tr.xpath('./td')
#     coinitem = CoinItem()
#     coinitem['num'] = tds[0].xpath('./text()').extract_first().strip()
#     coinitem['name'] = tds[1].xpath('./a/text()').extract_first().strip()
#     coinitem['symbol'] = tds[2].xpath('./text()').extract_first().strip()
#     coinitem['market_cap'] = tds[3].xpath('./text()').extract_first().strip()
#     coinitem['price'] = tds[4].xpath('./a/text()').extract_first().strip()
#     coinitem['circulating_supply'] = tds[5].xpath('string(.)').extract_first().strip().replace('\n*','')
#     coinitem['volume_24h'] = tds[6].xpath('./a/text()').extract_first().strip()
#     coinitem['change_percent_1h'] = tds[7].xpath('./text()').extract_first().strip()
#     coinitem['change_percent_24h'] = tds[8].xpath('./text()').extract_first().strip()
#     coinitem['change_percent_7d'] = tds[9].xpath('./text()').extract_first().strip()
#
#     print(coinitem)


# for tr in trs:
#     print()
#     tds = tr.xpath('./td/text()')
#     for td in tds:
#         print(td.extract().strip(),end='\t')
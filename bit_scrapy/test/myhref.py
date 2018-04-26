#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/7 上午11:11
# @Author  : zhujinghui 
# @site    : 
# @File    : test.py
# @Software: PyCharm
import requests
import json

# url = "http://v.myhref.com/api/v2/git/datas?callback=jQuery1113006754580325416071_1520391943084&sortBy=addCodesCountAWeek&_=1520391943085"

url = "http://v.myhref.com/api/v2/git/datas?sortBy=addCodesCountAWeek"

text = requests.get(url).text

data = text[5:-1]
data_json = json.loads(data)
# print(data_json)
infos = data_json['infos']
print(infos[0])
# for line in infos:
#     print(line)


with open('tmp.txt','w',encoding='utf-8') as f:
    for line in infos:
        f.write(repr(line)+'\n')



# 序号
# 代码
# 提交次数（近一个月）
# 提交次数（上周）
# 提交次数（本周）
# 代码量（近一个月
# 代码量（上周
# 代码量（本周
# 分支数
# 问题数
# 订阅数
# 关注数
# 项目库
# 编程语言
# 创建
# 提交
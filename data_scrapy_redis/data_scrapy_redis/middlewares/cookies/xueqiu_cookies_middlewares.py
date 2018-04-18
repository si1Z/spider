#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/17 10:06
# @Author  : zhujinghui
# @File    : xueqiu_cookies_middlewares.py
# @Software: PyCharm

from ...utils.cookie import XueQiuCookie
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

#雪球cookie
class CookiesMiddleware(RetryMiddleware):
    """ CHANGE COOKIE """
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        self.cookie = XueQiuCookie()
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        code,cookie = self.cookie.getCookie()
        request.cookies = cookie
        request.meta["code"] = code

    def process_response(self, request, response, spider):
        if response.status in [200]:
            return response
        elif response.status in [300,301,302,303]:
            try:
                redirect_url =  bytes.decode(response.headers["location"])
                if "/service/captcha" in redirect_url:
                    print('a'*30)
                    reason = response_status_message(response.status)
                    return self._retry(request, reason, spider) or response
                else:
                    reason = response_status_message(response.status)
                    return self._retry(request, reason, spider) or response
            except Exception as e:
                raise IgnoreRequest
        elif response.status in [403,414,400]:
            code = request.meta['code']
            self.cookie.upDateCookie(code)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        else:
            return response

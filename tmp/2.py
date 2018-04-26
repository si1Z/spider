#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 上午10:37
# @Author  : zhujinghui 
# @site    : 
# @File    : 2.py
# @Software: PyCharm
import socket
import _thread as thread
from urllib.parse import urlparse
import select


BUFLEN = 8192


class Proxy(object):
    def __init__(self, conn, addr):
        self.source = conn
        self.request = ""
        self.headers = {}
        self.destnation = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def get_headers(self):
        header = b''
        while True:
            header += self.source.recv(BUFLEN)
            print(header)
            index = header.find(b'\n')
            if index > 0:
                break
        # firstLine,self.request=header.split('\r\n',1)
        firstLine = header[:index]
        self.request = header[index + 1:]
        self.headers['method'], self.headers['path'], self.headers['protocol'] = firstLine.split()

    def conn_destnation(self):
        url = urlparse(self.headers['path'])
        hostname = url[1]
        port = "80"
        if hostname.find(b':') > 0:
            addr, port = hostname.split(':')
        else:
            addr = hostname
        port = int(port)
        ip = socket.gethostbyname(addr)
        print(ip, port)
        self.destnation.connect(('127.0.0.1', 1087))
        data = b"%s %s %s\r\n" % (self.headers['method'], self.headers['path'], self.headers['protocol'])
        self.destnation.send(data + self.request)
        print(data + self.request)

    def renderto(self):
        readsocket = [self.destnation]
        while True:
            data = ''
            (rlist, wlist, elist) = select.select(readsocket, [], [], 3)
            if rlist:
                data = rlist[0].recv(BUFLEN)
                if len(data) > 0:
                    self.source.send(data)
                else:
                    break
        # readsocket[0].close();

    def run(self):
        self.get_headers()
        self.conn_destnation()
        self.renderto()


class Server(object):

    def __init__(self, host, port, handler=Proxy):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        self.handler = handler

    def start(self):
        while True:
            try:
                conn, addr = self.server.accept()
                thread.start_new_thread(self.handler, (conn, addr))
            except:
                pass


if __name__ == '__main__':
    s = Server('10.8.233.197', 9888)
    s.start()
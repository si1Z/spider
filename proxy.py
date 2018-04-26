#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 下午2:29
# @Author  : zhujinghui 
# @site    : 
# @File    : proxy.py
# @Software: PyCharm
import socket
import threading
import select
from urllib.parse import urlparse

BUFLEN = 8192

class Proxy():
    def __init__(self, conn, addr):
        self.source = conn
        self.firstLine = b""
        self.request = b""
        self.headers = {}
        self.data = b""
        self.destnation = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.run()

    def get_headers(self):
        data = b''
        while True:
            data += self.source.recv(BUFLEN)
            index = data.find(b'\n')
            if index > 0:
                break

        print("x"*50)
        print(data)
        firstLine,self.request=data.split(b'\r\n',1)
        self.headers['method'], self.headers['path'], self.headers['protocol'] = firstLine.split()
        self.data = data

    def conn_destnation(self):
        url = urlparse(self.headers['path'])
        hostname = url[2]
        print(hostname)
        port = "80"
        if hostname.find(b':') > 0:
            addr, port = hostname.split(b':')
        else:
            addr = hostname
        port = int(port)
        ip = socket.gethostbyname(addr)

        print(ip, port)
        self.destnation.connect((ip, port))
        # data = b"%s %s %s\r\n" % (self.headers['method'], self.headers['path'], self.headers['protocol'])
        # self.destnation.send(self.firstLine + b'\r\n' + self.request)
        self.destnation.send(self.data)

    def renderto(self):

        readsocket = [self.destnation]
        while True:
            data = ''
            (rlist, wlist, elist) = select.select(readsocket, [], [], 3)
            if rlist:
                data = rlist[0].recv(BUFLEN)
                print(data)
                if len(data) > 0:
                    self.source.send(data)
                else:
                    break

        # while True:
        #     data = b''
        #     data= self.destnation.recv(BUFLEN)
        #     print(data)
        #     if len(data) > 0:
        #         self.source.send(data)
        #     else:
        #         break

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
                threading._start_new_thread(self.handler, (conn, addr))
                # thread.start_new_thread(self.handler, (conn, addr))
            except:
                pass

if __name__ == "__main__":
    s = Server('10.8.233.197', 9888)
    s.start()
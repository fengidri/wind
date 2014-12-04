# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-09-02 09:14:48
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import socket
import json
import re
import pyvim
import os
import time
#infos = {"type":"tag", "tag":[
#["vuirpc.h"        , "vuirpc.h"        , "vuirpc.h",        0],
#["rnetwork/anet.h" , "rnetwork/anet.h" , "rnetwork/anet.h", 0],
#["rnetwork/ae.h"   , "rnetwork/ae.h"   , "rnetwork/ae.h",   0],
#["network.h"       , "network.h"       , "network.h",       0],
#["rlist/adlist.h"  , "rlist/adlist.h"  , "rlist/adlist.h",  0],
#["client.h"        , "client.h"        , "client.h",        0],
#["cJSON/cJSON.h"   , "cJSON/cJSON.h"   , "cJSON/cJSON.h",   0],
#["vuiint.h"        , "vuiint.h"        , "vuiint.h"         ,   0]
#
#    
#    ]}
host = "127.0.0.1"
port =  7878

class ExceptionClosed(Exception):
    pass
class ExceptionReset(Exception):
    pass

class Response(object):
    def __init__(self, code, reason, msg):
        self.code = code
        self.reason = reason
        self.msg = msg

def handle100(response):
    pyvim.echoline(response.reason)

def handle110(response):
    pass

def handle200(response):
    pass

class VuiProctocol(object):
    def __init__(self, host, port):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in [1,2]:
            try:
                self.sock.connect((host, port))
                break
            except:
                os.popen2('vuirpc_server')
                time.sleep(1)

        self.buf = ""
    def _send(self, msg):
        self.sock.send(msg)

    def __recv(self):
        while True:
            try:
                buf = self.sock.recv(1024)
            except socket.error,e:
                if e.find("reset") > -1:
                    raise ExceptionReset("socket reset")
            if not buf:
                raise ExceptionClosed("socket closed")
            self.buf += buf
            if len(buf) != 1024:
                return self.buf
    def __reslove_packet(self):
        pos = 0
        buf = self.buf
        pos = buf.find("VPC/1.0", pos)
        if pos == -1:
            self.buf = ""
            return

        if pos != 0:
            buf = self.buf = buf[pos:]

        body = buf.find("\r\n\r\n")
        if body == -1:
            return # 没有找到包体, 继续读数据
        body += 4

        length = buf.find("length:")
        if length == -1 or length > body:
            pos = body
            return # 找到了body但是没有在头里找到length, 
        length_e = buf.find("\r\n", length)
        try:
            res_length = int(buf[length + 7: length_e])
        except:
            self.buf = buf[body:]
            return # 找到了body但是没有在头里找到length, 
        if len(buf) - body < res_length:
            return  # 包还没有取完


        regex = "^VPC\/1\.0 (\d+) (.*)\r\n"
        match = re.search(regex, buf)
        if not match:
            self.buf = buf[body:]
            return
        code = int(match.group(1))
        reason  = match.group(2)
        msg = buf[body: body+res_length]
        self.buf = buf[body+res_length:]
        return Response(code, reason, msg)

    def _recv(self):
        res = self.__reslove_packet()
        if res:
            return res
        while True:
            self.__recv()
            res = self.__reslove_packet()
            if res:
                return res
    def send(self, url,  json_msg):
        msg = json.dumps(json_msg)
        msg = "%s %s %s\r\nlength: %s\r\n\r\n%s" % (self.Method, url, 
                self.Version, len(msg), msg)
        self._send(msg)


class VuiClient(VuiProctocol):
    Method = "POST"
    Url    = "/"
    Version  = "VPC/1.0"
    def __init__(self, host=host, port=port):
        VuiProctocol.__init__(self, host,port)
        self.handle_map = {
                100: handle100,
                110: handle110,
                200: handle200
                }
    def gethandle(self, code):
        return self.handle_map.get(code)
    def sethandle(self, code, handle):
        self.handle_map[code] = handle

    def request(self, url, msg):
        self.send(url, msg)

    def response(self):
        res =  self.__loop()
        if not res:
            res = Response(500, "lost connect!", "")
        return res


    def __loop(self):
        while True:
            try:
                response = self._recv()
            except ExceptionClosed:
                print "closed"
                break

            if not response:
                continue
            handle = self.gethandle(response.code)
            if handle:
                handle(response)
            if response.code >= 200:
                return response





# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-09-16 07:10:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1



"""
Hammerspoon code:
================================================================================
function clipboard_handler(method, path, headers, body)
   if method == "GET"
   then
      return hs.pasteboard.getContents(),200, {}
   end
   if method == "POST"
   then
      res = hs.json.decode(body)
      if res["ops"] == "paste"
      then
	hs.pasteboard.setContents(res["paste"])
	return 'ok', 200, {}
      end

      if res["ops"] == "urlopen"
      then
        hs.execute("open " .. res["url"])
	return 'ok', 200, {}
      end
   end

   return '', 404,{}

end

server = hs.httpserver.new()
server:setInterface('loopback')
server:setPort(8082)
server:setCallback(clipboard_handler)
server:start()
================================================================================
"""

import vim
import pyvim
import sys
import os
import requests
import json
import re

class g:
    url = 'http://clipboard:8989/'


@pyvim.cmd()
def MacClipGet():
    setreg = vim.Function('setreg')
    setreg('"', '')
    res = requests.get(g.url, timeout=1)
#    text = res.text.decode('UTF8')

    c = res.text
    if vim.eval('&ft') == 'markdown':
        if c.startswith('http://') or c.startswith('https://'):
            res = requests.head(c)
            ct = res.headers.get('Content-Type')
            if ct.startswith('image/'):
                c = '![](%s)' % c
            else:
                c = '[...](%s)' % c

    if vim.eval('&ft') == 'plaintex':
        if c.startswith('http://') or c.startswith('https://'):
            res = requests.head(c)
            ct = res.headers.get('Content-Type')
            if ct.startswith('image/'):
                c = '\httpimg{%s}' % c
            else:
                c = c

    setreg('"', c)

@pyvim.cmd()
def MacClipPost():
    getreg = vim.Function("getreg")
    copy = getreg('"')

    j = {"ops": "paste", "paste": copy.decode('utf8')}

    requests.post(g.url, data = json.dumps(j), timeout=0.5)

@pyvim.cmd()
def MacURLOpen():
    line = vim.current.line
    urls = re.findall('https?://\S+', line)
    if not urls:
        return

    j = {"ops": "urlopen", "url": urls[0]}

    requests.post(g.url, data = json.dumps(j), timeout=0.5)


if __name__ == "__main__":
    pass


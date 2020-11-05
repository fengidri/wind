# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-09-16 07:10:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1



"""
Hammerspoon code:
================================================================================
function clipboard_callback(method, path, headers, body)
    if method == "GET"
    then
    	return hs.pasteboard.getContents() or "", 200, {}
    end
    hs.pasteboard.setContents(body)

    return '', 200, {}
end



server = hs.httpserver.new()
server:setCallback(clipboard_callback)
server:setInterface('127.0.0.1')
server:setPort(1542)
server:start()
================================================================================
"""

import vim
import pyvim
import sys
import os
import requests

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

    requests.post(g.url, data = getreg('"'), timeout=1)



if __name__ == "__main__":
    pass


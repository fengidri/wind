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


@pyvim.cmd()
def MacClipGet():
    res = requests.get("http://10.0.2.2:1542/")
#    text = res.text.decode('UTF8')
    setreg = vim.Function('setreg')
    setreg('"', res.text)

@pyvim.cmd()
def MacClipPost():
    getreg = vim.Function("getreg")
    copy = getreg('"')

    requests.post("http://10.0.2.2:1542/", data = getreg('"'))



if __name__ == "__main__":
    pass


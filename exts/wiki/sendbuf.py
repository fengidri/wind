# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-14 13:45:33
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import urllib
import urllib2
import pyvim
import vim

@pyvim.event("CursorHold", "*.mkiv")
@pyvim.event("CursorHoldI", "*.mkiv")
def SendBuf():
    ShowUrl = 'http://localhost/texshow/data'
    data = urllib.urlencode(
            {   "data": '\n'.join(vim.current.buffer),
                "type": "mkiv"})

    req = urllib2.Request(ShowUrl, data)
    try:
        urllib2.urlopen(req).read()
    except Exception, e:
        logging.error(e)

if __name__ == "__main__":
    pass


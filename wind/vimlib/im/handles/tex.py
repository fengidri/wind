# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-19 14:28:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import time
import re

from im import imutils
from im.imrc import feedkeys
import urllib
import urllib2
import vim
from pyvim import log as logging

ShowUrl = 'http://localhost/autofresh/data'

class IM_Tex( object ):
    def __init__(self):
        self.pmenu = pyvim.SelMenu()
        self.regex = re.compile(r"\\[a-zA-Z]+$")
        self.last_send_buf = time.time()

    def send(self):
        self.last_send_buf = time.time()

        data = urllib.urlencode({
            "data": '\n'.join(vim.current.buffer),
            "type": "mkiv"})

        req = urllib2.Request(ShowUrl, data)
        try:
            urllib2.urlopen(req).read()
        except Exception, e:
            logging.error(e)

    def event(self, ev):
        if not ev in ['CursorHold', 'CursorHoldI']:
            return

        self.send()
        return True

    def im(self, key):
        #t = time.time()
        #if t - self.last_send_buf > 2:
        #    logging.error('send.........')
        #    self.send()

        s = pyvim.str_before_cursor() + key
        match = self.regex.search(s)
        if not match:
            return False

        feedkeys(key)
        return True

    im_upper = im_lower = im

if __name__ == "__main__":
    pass


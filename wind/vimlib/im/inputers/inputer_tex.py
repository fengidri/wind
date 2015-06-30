# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-19 14:28:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from inputer_base import IM_Base 
import pyvim
import re
from im import imutils
from im.imrc import feedkeys

class IM_Tex( object ):
    def __init__(self):
        self.pmenu = pyvim.SelMenu()
        self.regex = re.compile(r"\\[a-zA-Z]+$")

    def im(self, key):

        s = imutils.key_to_see(key)
        if not (len(s) == 1 and s.isalpha()):
            return

        s = pyvim.str_before_cursor() + s
        match = self.regex.search(s)
        if not match:
            return False


        feedkeys(key)

        return True

if __name__ == "__main__":
    pass


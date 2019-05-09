# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 12:32:39
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
from pyvim import log
from .imrc import feedkeys

keyname = {
     "parenthess"  : "("       ,
     "bracket"     : "["       ,
     "brace"       : "{"       ,
     "mark"        : "'"       ,
     "comma"       : ","       ,
     "semicolon"   : ";"       ,
     "minus"       : "-"       ,
     "underline"   : "_"       ,
     "add"         : "+"       ,
     "precent"     : "%"       ,
     "and_"        : "&"       ,
     "lt"          : "<"       ,
     "gt"          : ">"       ,
     "cat"         : "^"       ,
     "not_"        : "!"       ,
     "dot"         : "."       ,
     "slash"       : "/"       ,
     "eq"          : "="       ,
     "double_mark" : '"'       ,
     "tab"         : '<tab>'   ,
     "backspace"   : '<bs>'    ,
     "enter"       : '<cr>'    ,
     "space"       : '<space>' ,
     "esc"         : '<esc>'   ,
     'jump'        : '<c-j>'   ,
}

class BasePass(object):
    """
        ALL the key will pass over. Use by the stream handle that just deal some
        keys.
    """
    def __init__(self):
        #处理重载的key
        self.cbs = {}
        for attr in dir(self):
            if not attr.startswith('cb_'):
                continue

            vname = keyname.get(attr[3:])
            if not vname:
                continue

            self.cbs[vname] = getattr(self, attr)

    def output(self, out):
        return False

    def run_handle(self, k):
        cb = self.cbs.get(k)
        if cb:
            return cb()
        else:
            return False


    im_digit = im_upper = im_lower = output
    im_punc  = im_mult  = run_handle



class BaseEnd(BasePass):
    " All the key will handle defaultly."
    def output(self, k):
        feedkeys(k)
        return True
    im_digit = im_upper = im_lower = output

    def im_punc(self, k):
        if not BasePass.run_handle(self, k):
            feedkeys(k)
        return True

    def im_mult(self, k):
        if not BasePass.run_handle(self, k):
            feedkeys('\%s' % k)
        return True

    def handler(self, tp, key):
        getattr(self, tp)(key)

if __name__ == "__main__":
    pass


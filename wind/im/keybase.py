# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 12:32:39
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
from pyvim import log
from .imrc import feedkeys
from . import env

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
     'digit0'        : '0'   ,
     'digit1'        : '1'   ,
     'digit2'        : '2'   ,
     'digit3'        : '3'   ,
     'digit4'        : '4'   ,
     'digit5'        : '5'   ,
     'digit6'        : '6'   ,
     'digit7'        : '7'   ,
     'digit8'        : '8'   ,
     'digit9'        : '9'   ,
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
            cb()
            return True
        else:
            return False


    im_digit = im_upper = im_lower = output
    im_punc  = im_mult  = run_handle



class BaseEnd(BasePass):
    " All the key will handle defaultly."
    def cb_jump(self):
        string = env.after

        tag=r'\'"([{}])'

        for i, c in enumerate(string):
            if c in tag:
                break

        if None == i:
            return True

#        if c == '"' or c == "'":
#            if i + 1 < len(string):
#                c = string[i + 1]
#                if c == ')' or c == ']':
#                    i = i + 1

        feedkeys( '\<right>' * (i +1))

        return True

    def cb_esc(self):
        feedkeys('\<esc>')
        return True

    def cb_backspace(self):
        feedkeys('\<bs>')
        return True # continue


    def output(self, k):
        if not BasePass.run_handle(self, k):
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


# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 15:14:23
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import im.imrc as imrc
from im.imrc import feedkeys

keyname = {
 "parenthess"       :      "("      ,
 "bracket"          :      "["      ,
 "brace"            :      "{"      ,
 "mark"             :      "'"      ,
 "comma"            :      ","      ,
 "semicolon"        :      ";"      ,
 "minus"            :      "-"      ,
 "underline"        :      "_"      ,
 "add"              :      "+"      ,
 "precent"          :      "%"      ,
 "and_"             :      "&"      ,
 "lt"               :      "<"      ,
 "gt"               :      ">"      ,
 "cat"              :      "^"      ,
 "not_"             :      "!"      ,
 "dot"              :      "."      ,
 "slash"            :      "/"      ,
 "eq"               :      "="      ,
 "double_mark"      :      '"'      ,
 "tab"              :      '<tab>'  ,
 "backspace"        :      '<bs>'   ,
 "enter"            :      '<cr>'   ,
 "space"            :      '<space>' ,
 "esc"              :      '<esc>'  ,
 'jump'             :      '<c-j>'  ,
}





class IM_Base( object ):
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
        feedkeys(out)

    im_digit = output
    im_upper = output
    im_lower = output

    def im_punc(self, k):
        cb = self.cbs.get(k)
        if cb:
            cb()
            return True
        else:
            feedkeys(k)
            return True

    def im_mult(self, k):
        cb = self.cbs.get(k)
        if cb:
            cb()
            return True
        else:
            feedkeys('\%s' % k)
            return True

    def im_event(self, ev):
        pass




if __name__ == "__main__":
    pass


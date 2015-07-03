# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:49:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import urllib2
import json

import pyvim
import im.imrc as imrc
from im.imrc import feedkeys

from inputer_base import IM_Base
import logging

from im.imutils import SelMenu
class _wubi_seach( object ):
    def __init__(self):
        self.cache={  }


    def search_from_db(self, patten):
        try:
            r = urllib2.urlopen("http://localhost/wubi/search?patten=%s" %
                patten)
            w = json.loads(r.read())
            self.cache[ patten ] = w
            return w
        except Exception, e:
            pyvim.echoline(str(e))
            return ([], [])


    def search( self , patten):
        '得到备选的字词'
        words= self.cache.get( patten )

        if  words:
            return words

        return self.search_from_db(patten)

    def setcount(self, patten, num):
        w, ass = self.cache.pop(patten)
        if len(w) -1 < num:
            return
        ww = w[num]
        url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
                ww.encode('utf8'))
        try:
            urllib2.urlopen(url)
        except Exception, e:
            pyvim.echoline(str(e))

    def wubi(self, patten):
        return self.result(patten, *self.search(patten))

    def result(self, patten, words, associate):
        '组成vim 智能补全要求的形式，这一步只是py形式的数据，vim要求是vim的形式'

        items=[{"word": " " ,"abbr":"%s                  " %  patten }]

        if len( patten ) > 4:
            return items

        i = 0
        for w in words:
            i += 1
            items.append({"word":w, "abbr":"%s.%s"%(i, w)})

        for w, k, c  in associate:
            i += 1
            items.append(
                    {"word":w,
                        "abbr":"%s.%s %s"%(i, w, k)}
                    )

        return items

class IM_Wubi( IM_Base, _wubi_seach):
    def __init__(self, areas = ['String', 'Comment']):
        IM_Base.__init__(self)
        _wubi_seach.__init__(self)
        self.index = 0
        self.buffer=[]
        self.pmenu = SelMenu()
        self.AREAS = areas


    def im(self, key):
        area = pyvim.syntax_area()

        if not (area in self.AREAS or '*' in self.AREAS):
            return
        logging.error("wubi:area: %s, %s", area, self.AREAS)

        self.key = key
        if imrc.count - self.index!= 1:  # 保证连续输入
            del self.buffer[:]
        self.index = imrc.count

        if key in self.cbs: #如果有对应的重载方法
            self.cbs.get(key)()



        return True

    def im_digit(self, key):
        if pyvim.pumvisible():

            self.setcount(self.patten, int(key) -1)
            word = self.pmenu.getselect(int(key)).get('word')
            pyvim.feedkeys(word, 'n')
            del self.buffer[:]
            return 0
        pyvim.feedkeys( self.key ,'n')

    def im_upper(self, key):
        del self.buffer[:]
        pyvim.feedkeys(key  ,'n')

    def im_lower(self, key ):
        self.buffer.append(key)
        self.patten = ''.join(self.buffer)
        self.pmenu.show(self.wubi(self.patten), 0)

    def cb_backspace(self):
        if not pyvim.pumvisible():
            pyvim.feedkeys('\<bs>', 'n')
            return 0

        if len( self.buffer ) > 1:
            self.buffer.pop()
            self.patten = ''.join(self.buffer)
            self.pmenu.show(self.wubi(self.patten), 0)
        else:
            del self.buffer[:]
            self.pmenu.cencel( )


    def cb_enter(self):
        if pyvim.pumvisible():
            bs = pyvim.str_before_cursor()
            if len(bs) > 0:
                if ord(bs[-1]) > 178:
                    pyvim.feedkeys(r'\<space>', 'n')
            pyvim.feedkeys(r'%s\<C-e>' % self.patten,'n')
            del self.buffer[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def cb_space(self):
        del self.buffer[:]
        if pyvim.pumvisible():
            word = self.pmenu.getselect(1).get('word')
            bs = pyvim.str_before_cursor()
            if len(bs) > 0:
                c = bs[-1]
                o = ord(c)
                if c in ',.!:;?' or \
                       65<= o <=90 or \
                       97<= o <=122 :
                       #48<= o <=57 or\
                    pyvim.feedkeys('\<space>', 'n')
            pyvim.feedkeys(word, 'n')
            return 0
        pyvim.feedkeys('\<space>', 'n')

    def cb_esc( self ):
        del self.buffer[:]
        pyvim.feedkeys( '\<esc>','n')


if __name__ == "__main__":
    pass


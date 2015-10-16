# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-17 13:33:01
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
#对于注释与typing 要在处理语法之前再进行一些处理, 
# 不然会与正常的语法处理形成干扰
# 这些处理的结构生成一个新的word, 本质上与word很相似
from words import Words, Word
import logging

def prehandler(ws):
    logging.info('************ prehandler ************')
    _ws = Words(ws.source)
    while True:
        w = ws.getword()
        if not w: break

        if w.name() == '%':
            end = '\n'
            l = ws.find(end).getword_byindex(-1).pos[2] - w.pos[2] + len(end) 
            w = Word(Word.TYPE_COMMENT, l, 'comment',  w.pos)
            _ws.append(w)

        elif w.name() == '\starttyping':

            end = '\stoptyping'
            l = ws.find(end).getword_byindex(-1).pos[2] - w.pos[2] + len(end) 
            w = Word(Word.TYPE_TYPING,   l, 'typing',w.pos)
            _ws.append(w)

        else:
            _ws.append(w)
            ws.update()

    return _ws




if __name__ == "__main__":
    pass


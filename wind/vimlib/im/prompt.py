# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-05 13:01:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

"""
   prompt 用于进行输入提示. 
   1. 外部调用
        由外部程序完成补全功能. wind 只是负责 prompt 的调用与 pop 菜单的处理.
        在 pop 菜单出现的情况下, 所做的事情也只有 <tab> 对于 item 的选择.

   2. 内部调用
   2.1 no session
       这种情况与外部的调用相似, 也是没有 session 的. 在 pop 菜单出现的情况
       也就是完成 <tab> 的行为. 

       由 wind 完成 prompt item 的生成. 但是由于没有 session, 所以 prompt 不会
       代理这个过程

       例如: path prompt.

   2.2 session
       目前只用于 wubi. 这种的行为是比较复杂的, prompt 还要代理 prompt item 的生
       成.

       

"""
_prompt = []

TYPE_OUTCALL = 0
TYPE_INTCALL = 1
TYPE_SESSION = 2

class PromptSession(object):
    def __init__(self, handle):
        self.buf = []
        self.index = 0
        self.handle = handle

    def active(self, key):
        if self.buf:
            del self.buf[:]

        self.buf.append(key)
        self.handle(self.buf)

    def cb_backspace(self):
        if len( self.bufr ) > 1:
            self.buf.pop()
            self.handle(self.buf)
            self.pmenu.show(self.wubi(self.patten), 0)
        else:
            del self.buf[:]
            self.pmenu.cencel( )

    def cb_enter(self):
        if pyvim.pumvisible():
            bs = pyvim.str_before_cursor()
            if len(bs) > 0:
                if ord(bs[-1]) > 178:
                    pyvim.feedkeys(r'\<space>', 'n')
            pyvim.feedkeys(r'%s\<C-e>' % self.patten,'n')
            del self.buf[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def cb_space(self):
        del self.buf[:]

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


def append_string(ppt):
    _prompt.append({"word": ppt})

def append_list(ppt):
    for x in ppt:
        if isinstance(x, dict):
            _prompt.append(x)

        elif isinstance(x, basestring):
            append_string(x)



def append(ppt):
    if isinstance(ppt, list):
        append_list(ppt)

    elif isinstance(ppt, basestring):
        append_string(ppt)

def build(word, attr = None):
    if attr:
        return {"word": word, "attr": attr}
    else:
        return {"word": word}

def abuild(word, attr = None):
    _prompt.append(build(word, attr))


if __name__ == "__main__":
    pass


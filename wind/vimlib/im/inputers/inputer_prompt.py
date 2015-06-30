# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-29 17:58:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import imrc
from imrc import feedkeys

__handle = None
__follow_mode = True # 跟随模式
def emit(event, *k):
    pass


class SelMenu( object ):
    "基于omnicomplete 包装成的SelMenu"
    "默认使用内部的complete function"
    "也可以指定omnicomplete function "

    omnifunc = "vimlib#SelMenuFunction"
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(SelMenu, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def check_omnifunc( self, func ):
        if vim.eval( '&l:omnifunc' ) != func:
            vim.command("let &omnifunc='%s'" % func)
            vim.command("let &l:omnifunc='%s'" % func)

    def showlist(self, words_list, length):
        """ 与show 比较相似, 只是使用 输入的是list, 也就说是比较简单的结构"""
        words = []
        for w in words_list:
            words.append({"word": w})
        self.show(words, length)



    def complete(self, fun):
        "指定补全函数"
        self.check_omnifunc(fun)
        imrc.feedkeys('\<C-X>\<C-O>\<C-P>')

    def select(self, nu):
        if pumvisible( ):
            feedkeys((nu + 1) * '\<C-N>' , 'n' )
            imrc.feedkeys('\<C-Y>')

    def getselect(self, nu):
        if pumvisible( ):
            imrc.feedkeys('\<C-Y>')
        return self.words[nu]

    def cencel( self ):
        imrc.feedkeys('\<C-e>')

    def show(self, words, length):
        """使用内部的补全函数进行输出
                @words:   vim 格式的数据结构
                @length:  光标前要进行补全的字符长度
        """
        self.words = words
        vim.vars["omniresult"] = words
        vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1
        self.complete(self.omnifunc)


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


class prompt_handle(object):
    def cb_backspace(self):
        if len(self.buffer) > 1:
            self.buffer.pop()
            self.pmenu.show(self.get_prompt(), 0)
        else:
            self.close()
            self.pmenu.cencel( )


    def cb_enter(self):
        patten = ''.join(self.buffer)
        pyvim.feedkeys(r'%s\<C-e>' % patten,'n')
        self.close()

    def cb_space(self):
        word = self.pmenu.getselect(1).get('word')
        bs = pyvim.str_before_cursor()
        emit("Insert")
        pyvim.feedkeys(word, 'n')
        self.close()

    def cb_esc( self ):
        self.close()
        imrc.feedkeys('\<esc>')

    def digit( self ):
        word = self.pmenu.getselect(int(self.key)).get('word')
        pyvim.feedkeys(word, 'n')
        del self.buffer[:]

    def upper_letter( self ):
        del self.buffer[:]
        pyvim.feedkeys(self.key  ,'n')

    def lower_letter( self ):
        self.buffer.append( self.key )
        self.patten = ''.join(self.buffer)
        self.pmenu.show(self.get_prompt(), 0)

class IM_Wubi(prompt_handle):
    def __init__(self):
        self.index = 0
        self.buffer=[]
        self.pmenu = pyvim.SelMenu()
        self.follow = True

    def get_prompt(self):
        return emit("Get", ''.join(self.buffer))

    def close(self):
        del self.buffer[:]

    def im(self, key):
        if not pyvim.pumvisible():
            return False

        self.key = key
        if imrc.count - self.index != 1:  # 保证连续输入
            del self.buffer[:]
        self.index = imrc.count


        if key in imrc.digits:
            self.digit()

        elif key in imrc.lowerletter:
            self.lower_letter()

        elif key in imrc.upperletter:
            self.upper_letter()

        elif key in ['backspace', 'enter', 'space', 'esc']:
            getattr(self, 'cb_%s' % key)()
        return True


if __name__ == "__main__":
    pass


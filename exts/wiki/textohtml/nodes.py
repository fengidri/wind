# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:46
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from words import Word
import logging

class LostParamsEx(Exception):
    def __init__(self, word):
        print "%s:%s Lost Param" % (word.pos[0], word.pos[1])

class node_text(object):
    def __init__(self, ws):
        self.word = ws.getword()
        self.context = ws.getcontext(self.word)

        ws.update()

    def html(self):
        return self.context

    md = html

class node_cpunc(object): # 形如: \%
    def __init__(self, ws):
        self.word = ws.getword()
        self.context = ws.getcontext(self.word)[1:2]

        ws.update()

    def html(self):
        return self.context
    md = html

class node_comment(object):
    def __init__(self, ws):
        ws.update()

    def html(self):
        return ''
    md = html

class node_typing(object):
    def __init__(self, ws):
        s = len('\starttyping')
        e = len('\stoptyping')
        self.word = ws.getword()
        ws.update()
        self.context = ws.getcontext(self.word)[s: -1 * e]

    def html( self ):
        tp = self.context

        tp = tp.replace('&', "&amp;" )
        tp = tp.replace(  '<', '&lt;' )
        tp = tp.replace(  '>', '&gt;' )
        return "<pre>%s</pre>\n" %  tp

    def md( self ):
        tp = self.context

        tp = tp.replace('&', "&amp;" )
        tp = tp.replace(  '<', '&lt;' )
        tp = tp.replace(  '>', '&gt;' )
        return "\n```\n%s\n```\n" %  tp

class node_punc(object):
    def __init__(self, ws):
        self.word = ws.getword()
        word = self.word

        self.name =  self.word.name()

        if self.name == '%':
            ws.find('\n')
            self.h =  ''

        elif self.name == ' ':
            _ws, e = ws.find_same(' ')
            if e:# 忽略最后空格
                self.h = ''
            else:
                self.h =  ' '

        elif self.name == '\n':
            _ws, e = ws.find_same('\n')
            if e:# 忽略最后换行
                self.h = ''
            elif len(_ws) > 1:
                self.h = None
            else:
                self.h = '\n'

        elif self.name == '$':
            #TODO
            ws.find('$')
            self.h = ''

        else:
            self.h = self.name
            ws.update()


    def html(self):
        if self.h == None:
            return "</p>\n\n<p>"
        return self.h

    def md(self):
        if self.h == None:
            return "\n\n"
        return self.h

class node_control(object):
    """
        1. 控制序列后面出现的{}, [], 一定会被处理掉
        2. 控制序列后面出现的\n, space 也会被处理掉
    """
    def __init__(self, ws):
        self.ws = ws
        self.Params = []
        self.Attrs  = []

        #list.__init__(self)
        self.word = ws.getword()
        self._getattrs(ws)
        self._getparams(ws)
        self.init(ws)

    def init(self, ws):
        ws.update()

    def html(self):
        return ''
    md = html
    def _getparams(self, ws): # 得到参数, 参数可以有多个, {}
        self.__get_params_or_attrs(ws, '{', '}', self.Params)

    def _getattrs(self, ws): # 得到属性, 也可以有多个, []
        self.__get_params_or_attrs(ws, '[', ']', self.Attrs)

    def __get_params_or_attrs(self, ws, s, e, cb):
        #TODO
        first_lf = None
        while True:
            ws.update()
            word = ws.getword()
            if not word:
                break

            name = word.name()

            if name == ' ': continue # 中间所有的空格都是无视的

            elif name == '\n':
                if first_lf == None: # 记录第一个回车的位置
                    first_lf = ws.getpos()
                    continue
                else: # 第二个回车退出
                    break

            elif name == s:
                ps = ws.findnesting(e, nesting=s)
                p = node_tree(ps.slice(1, -1))
                cb.append(p)

                ws.back()
                first_lf = None
            else:
                ws.back()
                break
        if first_lf:#遇到过换行, 重新指向换行
            ws.initpos(first_lf)


class Section( node_control ):
    def init(self, ws):
        ws.update()
        self.name = self.word.name()

    def md(self):
        name = self.name
        level = name.count('sub') + 3

        if not self.Params:
            raise LostParamsEx(self.word)

        c = self.Params[0].html()
        return "\n%s %s\n" % ('#' * level, c)

    def html( self ):
        name = self.name
        level = name.count('sub') + 3

        if not self.Params:
            raise LostParamsEx(self.word)

        c = self.Params[0].html()
        h = "\n<h%s>%s</h%s>\n" % (level, c, level)
        return h




class Itemize( node_control ):
    def init(self, ws):
        _ws = ws.findnesting("\stopitemize", nesting='\startitemize', inside = False)
        self.tree = node_tree(_ws.slice(0, -1))

    def md(self):
        return "\n  %s" % self.tree.html()

    def html(self ):
        return "\n    <ul>\n%s\n    </ul>" % self.tree.html()


class Item( node_control ):
    def md(self):
        if self.Params:
            return '\n* %s' % self.Params[0].md()
        return '\n  '

    def html( self ):
        if self.Params:
            return '\n<li><b>%s</b>&nbsp;&nbsp;&nbsp;&nbsp;' % self.Params[0].html()
        return '\n        <li>'


class Goto( node_control ):
    def md( self ):
        name = self.Params[0].md()
        if len(self.Params) == 1:
            url = name
        else:
            url = self.Params[1].md()

        return "[%s](%s)" % (name, url)

    def html( self ):
        name = self.Params[0].md()
        if len(self.Params) == 1:
            url = name
        else:
            url = self.Params[1].md()

        return "&nbsp;<a href=%s >%s</a>&nbsp;" % (url, name)

class Img( node_control ):
    def html( self ):
        #TODO
        return "<img src=%s >" % (self.Params[0].html())

    def md( self ):
        #TODO
        return "![img](%s)" % (self.Params[0].html())

class Par( node_control ):
    def html( self ):
        return "<br />"

    def md( self ):
        return "\n\n"

class starttable(node_control):
    def html( self ):
        return "<table>\n"

    def md( self ):
        return "<table>\n"

class stoptable(node_control):
    def html( self ):
        return "</table>\n"

    def md( self ):
        return "\n"

class NC(node_control):
    def html( self ):
        return  "<tr><td>"

    def md( self ):
        return  "\n"

class AR(node_control):
    def html( self ):
        return  "</td></tr>\n"

    def md( self ):
        return  "\n"

class VL(node_control):
    def html( self ):
        return "</td><td>"

    def md( self ):
        return "|"


class Bold(node_control):
    def html(self):
        if len(self.Params) > 0:
            return "<b>%s</b>" % self.Params[0].html()
        return ""

    def md(self):
        if len(self.Params) > 0:
            return "`%s`" % self.Params[0].md()
        return ""

class Newline(node_control):
    def html(self):
        return "</p>\n\n<p>"

    def html(self):
        return "\n\n"

class DefHandle(node_control):
    MAPS = {}
    def init(self, ws):
        ws.update()
        name = self.word.name()
        self.de = self.MAPS.get(name)
        if not self.de:
            raise Exception("Dont know: %s@%s, %s" % (name,
                self.word.pos[0], self.word.pos[2]))

    def html(self):
        return self.de.Params[0].html()

class Def(node_control):
    def init(self, ws):
        while True:
            ws.update()
            word = ws.getword()
            name = word.name()
            if name in ['\n', ' ']:
                continue
            if word.type == Word.TYPE_CONTROL:
                self._getattrs(ws)
                self._getparams(ws)
                DefHandle.MAPS[name] = self
                break
        ws.update()

    def html(self):
        return ''

class backslash(node_control):

    def html(self):
        return '\\'



NODE_MAP={
        '\section'       : Section,
        '\subsection'    : Section,
        '\subsubsection' : Section,
        '\startitemize'  : Itemize,
        '\item'          : Item,
        '\goto'          : Goto,
        '\img'           : Img,
        '\par'           : Newline,
        '\starttable'    : starttable,
        '\stoptable'     : stoptable,
        '\NC'            : NC,
        '\VL'            : VL,
        '\AR'            : AR,
        '\\bold'         : Bold,
        '\\def'          : Def,
        '\\backslash'            : backslash,
                }

class node_tree(list):
    handlemap = {
            Word.TYPE_PUNC:    node_punc,
            Word.TYPE_TEXT:    node_text,
            Word.TYPE_CPUNC:   node_cpunc,
            Word.TYPE_COMMENT: node_comment,
            Word.TYPE_TYPING:  node_typing,
            }
    def __init__(self, ws):
        # 跳过开头的空白
        logging.debug("node tree: from %s to %s" , ws.start, ws.end)
        while True:
            w = ws.getword()
            if not w:
                break
            if not w.name() in ['\n', ' ']:
                break
            ws.update()

        while True:
            w = ws.getword()
            if not w:
                break
            logging.debug("node tree: scan word: %s, pos: %s, end: %s, wpos: %s",
                    w.showname(), ws.pos, ws.end, w.pos)

            cb = self.handlemap.get(w.type)
            if cb: self.append(cb(ws))

            elif w.type == Word.TYPE_CONTROL:
                callback = NODE_MAP.get(w.name())
                if not callback:
                    callback = DefHandle
                self.append(callback(ws))

        logging.debug("node tree exit: from %s to %s @ %s" , ws.start, ws.end,
                ws.pos)

    def html(self):
        h = [n.html() for n in self]
        return ''.join(h)

    def md(self):
        h = [n.md() for n in self]
        return ''.join(h)



if __name__ == "__main__":
    pass


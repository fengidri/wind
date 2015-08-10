# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 09:30:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import pyvim
import utils
import vim
import im



def match(pattern, source):
    length = len(pattern)
    index = 0
    m = 0

    if index >= length:
        return -1

    p = ord(pattern[index])
    for o, s in enumerate(source):
        tt = p - ord(s)
        if tt == 0 or tt == 32:
            m += o
            index += 1
            if index >= length:
                return m

            p = ord(pattern[index])
    else:
        return -1

def match_lines(pats, ng_pats, lines, mx = None):
    tmp = []
    index = 0
    if mx == None:
        mx = len(lines)

    for line in lines:
        for pat in ng_pats:
            if pat in line:
                break
        else:
            for pat in pats:
                if not pat in line:
                    break
            else:
                index += 1
                if index >= mx:
                    return tmp
                tmp.append(line)
    return tmp



class SearchWIN(Object):
    def show_list(self, lines, num=15):
        del self.buf.b[1:]
        if not lines:
            return
        num = min(len(lines), num)
        index = 1
        for i in range(0, num):
            line = lines[i]
            self.buf.b.append("  %s" % line, index)
            index += 1

    def hi_pats(self, pats):
        fadd = vim.Function('matchadd')
        fdel = vim.Function('matchdelete')
        for i in self.match_id:
            try:
                fdel(i)
            except:
                pass

        del self.match_id[:]

        for pat in pats:
            i = fadd('keyword', pat)
            self.match_id.append(i)

    def show(self):
        self.buf.show()

class BufferEvent(object):
    def buf_active(self, buf):
        l, c = vim.current.window.cursor
        l = l - 1
        if l == 0:
            self.match_line = ''
        else:
            self.match_line = self.buf.b[l].strip()

        im.async('frainui', 'search-quit')


    def buf_quit(self, buf):
        # 退出 search 模式
        vim.current.window = self.edit_win

        self.FREventEmit("quit", self.match_line)

        self.buf.delete()
        self.enter.delete()

class EnterEvent(object):
    def enter_active(self, enter):
        text = enter.get_text()
        num = 1
        tt = text.split(';')
        if len(tt) > 1:
            tt = tt[-1].strip()
            if tt.isdigit():
                num = int(tt)
                if num >= len(self.buf.b):
                    num = 1

        self.match_line = self.buf.b[num].strip()
        # 进入异步模式
        im.async('frainui', 'search-quit')

    def enter_change(self, enter, c):
        if c.find(';') > -1:
            return

        if c.find('$') > -1:
            im.async('frainui', 'search-quit')
            return

        pats = []
        ng_pats = []
        for pat in c.split():
            if pat[0] == '-':
                pat = pat[1:]
                if pat:
                    ng_pats.append(pat[1:])
            else:
                pats.append(pat)

        lines = match_lines(pats, ng_pats, self.lines, 20)
        self.show_list(lines)
        self.hi_pats(pats)


class Search(SearchWIN, BufferEvent, EnterEvent):
    def __init__(self, lines, name='search'):
        import Buffer
        import enter

        self.lines = lines
        self.match_line = None
        self.match_id = []
        self.name = name

        self.edit_win = vim.current.window

        self.FRRegister(name)

        self.buf = Buffer.Buffer(title = "Search", ft="frainuiSearch")
        self.buf.show()


        self.enter = enter.EnterLine(self.buf, 0, "Search:")

        self.enter.FREventBind("change", self.enter_change)
        self.enter.FREventBind("active", self.enter_active)

        self.buf.FREventBind("search-active", self.buf_active)
        self.buf.FREventBind("search-quit",   self.buf_quit)

        self.enter.FRInputFocus()

        self.show_list(lines)










if __name__ == "__main__":
    pass


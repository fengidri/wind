# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 09:30:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import pyvim
from  . import utils
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
    tmp_no = []
    index = 0
    if mx == None:
        mx = len(lines)

    for no, line in enumerate(lines):
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
                    return tmp, tmp_no
                tmp.append(line)
                tmp_no.append(no)
    return tmp, tmp_no



class SearchWIN(object):
    def show_list(self, lines, num=15):
        del self.BFb[1:]
        if not lines:
            return
        num = min(len(lines), num)
        index = 1
        for i in range(0, num):
            line = lines[i]
            self.BFb.append("%2d. %s" % (i + 1, line), index)
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
            self.match_id.append(fadd('keyword', pat))


class BufferEvent(object):
    def option_active(self, buf): # option_active
        l, c = vim.current.window.cursor
        l = l - 2

        self.match_line = -1
        if l >= 0:
            if self.nos:
                if l < len(self.nos):
                    self.match_line = self.nos[l]
            else:
                if l < len(self.lines):
                    self.match_line = l

        im.async_feed('frainui', 'OP-Quit')


    def quit(self, t = None):
        # 退出 search 模式
        if t:#OP-Quit
            vim.current.window = self.edit_win

        #if self.match_line and len(self.match_line) > 5:
        #    line = self.match_line[3:]
        #else:
        #    line = ''

        self.FREventEmit("Search-Quit", self.match_line)

        self.enter.delete()
        self.BFWipeout()
#        pyvim.delevent(self.h)

class EnterEvent(object):
    def enter_active(self, enter):
        self.match_line = 0
        if self.nos:
            self.match_line = self.nos[0]# self.BFb[1].strip()

        # 进入异步模式
        im.async_feed('frainui', 'OP-Quit')

    def enter_change(self, enter):
        pats = []
        ng_pats = []

        for pat in enter.get_text().split():
            if not pat:
                continue

            if pat[0] == '-':
                pat = pat[1:]
                if pat:
                    ng_pats.append(pat)
                else:
                    return
            else:
                pats.append(pat)

        lines, nos = match_lines(pats, ng_pats, self.lines, 100)
        self.nos = nos
        self.show_list(lines)
        self.hi_pats(pats)




from . import Buffer
class Search(Buffer.BF, SearchWIN, BufferEvent, EnterEvent):
    def __init__(self, lines, name='search'):
        Buffer.BF.__init__(self)
        self.lines = lines
        self.match_line = None
        self.match_id = []
        self.nos = [] # the show lines index in the origin list
        self.name = name

        self.edit_win = vim.current.window

        self.FRRegister(name)

        self.BFFt       = "frainuiSearch"
        self.BFName     = "Search"
        self.BFCreate()

        from .enter import EnterLine
        self.enter = EnterLine(self, 0, "Search:")
        self.enter.FREventBind("Enter-Active", self.enter_active)
        self.enter.FREventBind("Enter-Change", self.enter_change)

        self.FREventBind("OP-Active", self.option_active)
        self.FREventBind("OP-Quit", self.quit)

        self.BFSetImFocus(self.enter)

        self.show_list(lines)






if __name__ == "__main__":
    pass


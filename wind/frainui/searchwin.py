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



class SearchWIN(utils.Object):
    def enter_change(self, enter, c):
        if c.find(';') > -1:
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

    def show_list(self, lines, num=15):
        del self.buf.b[1:]
        if not lines:
            return
        num = min(len(lines), num)
        for i in range(0, num):
            line = lines[i]
            self.buf.b.append("  %s" % line, 1)

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


    def active(self, enter):
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
        im.async('frainui', 'vimquit', self.name)


    def quit(self, enter):
        vim.current.window = self.edit_win

        self.FREventEmit("quit", self.match_line)

        self.buf.delete()
        self.enter.delete()

    def show(self):
        self.buf.show()



class Search(SearchWIN):
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
        self.enter.FREventBind("active", self.active)

        self.FREventBind("vimquit", self.quit)

        self.enter.FRInputFocus()

        self.show_list(lines)










if __name__ == "__main__":
    pass


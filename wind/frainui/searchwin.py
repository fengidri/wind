# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 09:30:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import pyvim
import utils
import vim

def match_lines(pats, lines):
    tmp = []
    for line in lines:
        for pat in pats:
            if not pat in line:
                break
        else:
            tmp.append(line)
    return tmp



class SearchWIN(utils.Object):
    def __init__(self, lines):
        import Buffer
        import enter
        self.buf = Buffer.Buffer(title = "Search", ft="frainuiSearch")
        self.buf.show()

        self.enter = enter.EnterLine(self.buf, 0, "Search:")
        self.enter.FRInputFocus()
        self.enter.FREventBind("change", self.enter_change)
        self.enter.FREventBind("active", self.active)
        self.enter.FREventBind("quit", self.quit)

        self.lines = lines
        #import tree
        #self.tree  = tree.Tree(self.buf, 2, 15)
        self.show_list(lines)

        self.match_line = None

    def show_list(self, lines, num=15):
        num = min(len(lines), num)
        for i in range(0, num):
            line = lines[i]
            self.buf.b.append(line, 1)


    def enter_change(self, enter, c):

        pats = c.split()
        lines = match_lines(pats, self.lines)
        del self.buf.b[1:]

        self.show_list(lines)


        fadd = vim.Function('matchadd')

        vim.command("clearmatches()")

        for pat in pats:
            fadd('keyword', pat)


    def active(self, enter):
        self.match_line = self.buf.b[1]

    def quit(self, enter):
        self.FREventEmit('quit', self.match_line)











if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-30 09:40:15
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import im.imrc
import pyvim
import vim
import re

class CSameChange(object):
    _instance = None
    def __init__(self):
        be, af = self.cur_word()

        self.indent = self.get_indent(vim.current.line)

        cursor          = vim.current.window.cursor
        self.sc_linenu  = cursor[0]
        self.sc_col     = cursor[1]  - len(be)
        self.pos        = self.get_pos(cursor[0], be + af)
        pyvim.log.error(self.pos)
        self.length     = len(be) + len(af)

        self.evhandle1 = pyvim.addevent('CursorMovedI', self.change)
        self.evhandle2 = pyvim.addevent('InsertLeave',  self.exit)

        SameChange._instance = self

    def exit(self):
        SameChange._instance = None
        buf = []
        for c in vim.current.buffer[self.sc_linenu - 1][self.sc_col:]:
            if c.isalpha() or c == '_':
                buf.append(c)
            else:
                break

        self.sm_change(''.join(buf))
        pyvim.delevent(self.evhandle1)
        pyvim.delevent(self.evhandle2)

    def change(self):
        linenu, col = vim.current.window.cursor
        pyvim.log.error('%s %s %s %s', linenu, col, self.sc_linenu, self.sc_col)
        if linenu != self.sc_linenu:
            self.exit()
            return

        be = vim.current.line[self.sc_col: col]
        be, af = self.cur_word()
        pyvim.log.error("be: %s af: %s", be, af)
        if len(be) != col - self.sc_col:
            self.exit()
            return

        self.sm_change(be + af)



    def sm_change(self, word):
        length = len(word)
        pos_offset = length - self.length
        for linenu, cols in self.pos.items():
            pyvim.log.error('%s %s', linenu, cols)
            line = vim.current.buffer[linenu]

            offset = 0
            tt = []
            for c in cols:
                tt.append(line[offset: c])
                offset = c + self.length
            tt.append(line[offset: ])

            for i, c in enumerate(cols):
                cols[i] = cols[i] + pos_offset * i



            vim.current.buffer[linenu] = word.join(tt)
        self.length = len(word)


    def get_indent(self, line):
        m = re.search('^(\s+)', line)
        if not m:
            return 0
        return len(m.group(1))

    def get_pos(self, linenu, word):
        pos = {}
        if len(vim.current.buffer) <= linenu:
            return pos

        regex = r'\b%s\b' % word
        for i, line in enumerate(vim.current.buffer[linenu:]):
            pyvim.log.error("%s, %s", self.indent, self.get_indent(line))
            indent = self.get_indent(line)

            if indent == len(line):
                continue

            if indent <= self.indent:
                break

            pyvim.log.error("word: %s" % regex)
            pyvim.log.error("word: %s" % line)

            line_pos = [it.span()[0] for it in re.finditer(regex, line)]
            if line_pos:
                pos[i+linenu] = line_pos

        return pos



    def cur_word(self):
        before_str = pyvim.str_before_cursor()
        after_str = pyvim.str_after_cursor()

        be_match = re.search('(\w+)$', before_str)
        af_match = re.search('^(\w+)', after_str)

        if be_match:
            be_str = be_match.group(1)
        else:
            be_str = ''

        if af_match:
            af_str = af_match.group(1)
        else:
            af_str = ''

        return (be_str, af_str)




@pyvim.cmd()
def SameWord():
    if CSameChange._instance:
        return
    CSameChange()


if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim


class C_Marco(object):
    def __init__(self):
        tabstop = int(vim.eval('&tabstop'))
        exptab = int(vim.eval('&expandtab'))

        nu = self.lookup_first_marco_linenu()
        if nu == None:
            return

        lines, width = self.lookup_marco_lines(nu, tabstop)

        for line, w in lines:
            if (width - w) % tabstop:
                n = (width - w) / tabstop + 1
            else:
                n = (width - w) / tabstop

            n = int(n)

            line = line + '\t' * n + '\\'

            vim.current.buffer[nu] = line
            nu += 1

    def is_marco_line(self, line):
        if not line:
            return None

        line = line.rstrip()

        if not line or line[-1] != '\\':
            return None

        line = line[0: -1]
        line = line.rstrip()
        return line

    def lookup_first_marco_linenu(self):
        cursor = vim.current.window.cursor
        nu = cursor[0] - 1

        line = vim.current.buffer[nu]
        if not self.is_marco_line(line):
            return

        nu -= 1
        if nu == 0:
            return 0

        while True:
            line = vim.current.buffer[nu]
            if None == self.is_marco_line(line):
                nu += 1
                break

            if nu == 0:
                break

            nu -= 1

        return nu

    def lookup_marco_lines(self, nu, tabstop):
        lines = []
        width = 0

        while True:
            line = vim.current.buffer[nu]
            nu += 1

            line = self.is_marco_line(line)
            if None == line:
                break

            w = len(line)
            w += (tabstop - 1) * line.count('\t')

            lines.append((line, w))

            if width < w:
                width = w

        if width % tabstop:
            width = int(width / tabstop + 1) * tabstop
        else:
            width = int(width / tabstop) * tabstop

        return lines, width

@pyvim.cmd()
def AlignMarco():
    C_Marco()



def is_ignore_word(s):
    iws = set(['const', 'unsigned', 'struct', 'enum'])
    t = set(s.split())

    if len(t - iws) == 0:
        return 1

    return 0


class Line(list):
    def __init__(self, s):
        list.__init__(self)

        self.index = 0
        self.cols = 0
        self.index_char = ' '

        for c in s:
            if c == ' ' or c == '\t':
                self.index_char = c
                self.index += 1
            else:
                break

        self.string = s.strip()
        self.split()

    def split(self):
        start = 0

        skip_white = 0
        cp = None

        for i,s in enumerate(self.string):
            if cp:
                if cp == s:
                    cp = None
                continue

            if skip_white:
                if s in ' \t':
                    continue
                else:
                    skip_white = 0
                    start = i

            if s == '=':
                w = self.string[start: i]
                if w:
                    self.append(item(w, start))
                self.append(item(s, i))
                skip_white = 1
                continue

            if s in ' =\t':
                w = self.string[start: i]
                if is_ignore_word(w):
                    continue

                self.append(item(w, start))
                skip_white = 1
                continue

            if s == '"' or s == "'":
                cp = s
        w = self.string[start:]
        self.append(item(w, start))

    def s(self):
        l = [self.index_char * self.index ]
        for ii, i in enumerate(self):
            i.index = ii
            i.cols = self.cols
            i.line = self.string
            l.append(i.s())

        pyvim.log.error(l)
        return ''.join(l)



class item(object):
    def __init__(self, s, pos):
        self.padding = 0
        self.index = 0
        self.cols = 0
        self.pos = pos

        for c in s:
            if c == '*':
                self.padding += 1
            else:
                break

        self.width  = len(s)
        self.string = s
        self.line   = None

    def s(self):
        if self.index > 0:
            self.padding += 1

        if self.index > self.cols - 1:
            return ""

        elif self.index == self.cols - 1:
            return "%s%s" % (' ' * self.padding, self.line[self.pos:])

        else:
            return "%s%s" % (' ' * self.padding, self.string.ljust(self.width))






def _align_col(col):
    width = 0
    padding = 0

    for i in col:
        padding = max(padding, i.padding)
        width   = max(width,   i.width + i.padding)

    for i in col:
        i.padding = padding - i.padding
        i.width   = width - i.padding

def _align(lines):
    cols = 99999

    for l in lines:
        cols = min(cols, len(l))

    for l in lines:
        l.cols = cols;

    if cols < 2:
        pyvim.echo("cols %d", cols)
        return

    for i in range(cols):
        _align_col([l[i] for l in lines if l.cols])







@pyvim.cmd()
def Align(tag = ' '):
    pos1, pos2 = pyvim.selectpos()
    line1 = pos1[0]
    line2 = pos2[0] + 1
    lines = vim.current.buffer[line1: line2]

    L = []
    for line in lines:
        l = Line(line)
        l.linenu = line1
        line1 += 1

        if len(l) < 2:
            continue

        L.append(l)


    _align(L)

    for l in L:
        vim.current.buffer[l.linenu] = l.s()



# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim




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

        for c in s:
            if c == ' ' or c == '\t':
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
        l = [' ' * self.index ]
        for ii, i in enumerate(self):
            i.index = ii
            i.cols = self.cols
            i.line = self.string
            l.append(i.s())

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

        self.width = len(s) - self.padding
        self.string = s
        self.line = None

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
    padding = 0
    width = 0

    for i in col:
        padding = max(padding, i.padding)
        width   = max(width,   i.width)

    for i in col:
        i.padding = padding - i.padding
        i.width   = width





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
        _align_col([l[i] for l in lines])







@pyvim.cmd()
def Align(tag = ' '):
    pos1, pos2 = pyvim.selectpos()
    line1 = pos1[0]
    line2 = pos2[0] + 1
    lines = vim.current.buffer[line1: line2]

    lines = [Line(line) for line in lines]

    _align(lines)

    vim.current.buffer[line1: line2] = [line.s() for line in lines]



# -*- coding:utf-8 -*-

import vim
from pyvim import log
import pyvim

class vimfun:
    setwinvar = vim.Function("setwinvar")
    win_execute = vim.Function("win_execute")


class popup:
    winids = {}
    create = vim.Function("popup_create")
    close = vim.Function("popup_close")
    settext = vim.Function("popup_settext")
    setoptions = vim.Function("popup_setoptions")

def handle(winid, key):
    winid = int(winid)
    p = popup.winids.get(winid)
    if not p:
        return

    p.handle(int(key))

class Popup(object):
    def create(self, what, opt):
        self.winid = popup.create(what, opt)
        self.bufid = vim.eval('winbufnr(%s)' % self.winid)

        popup.winids[self.winid] = self

        vimfun.setwinvar(self.winid, '&wincolor', 'Normal')


        cmd = 'call setbufvar(winbufnr(%s), "&filetype", "popup")' % self.winid
        vim.command(cmd)

#        cmd = 'echo getbufvar(winbufnr(%s), "&tm")' % self.winid
#        vim.command(cmd)
#
#        cmd = 'echo getbufvar(winbufnr(%s), "&ttm")' % self.winid
#        vim.command(cmd)
#
#        cmd = 'echo getbufvar(winbufnr(%s), "&ek")' % self.winid
#        vim.command(cmd)

    def command(self, cmd):
        vimfun.win_execute(self.winid, cmd)

    def setpos(self, line, col = 0):
        self.command("call setpos('.', [0, %s, %s,0])"% (line, col))

    def close(self):
        popup.close(self.winid)

    def settext(self, text):
        popup.settext(self.winid, text)

    def setoptions(self, opt):
        popup.setoptions(self.winid, opt)

    def handle(self, key):
        pass

class Line(object):
    def __init__(self, prompt = '>'):
        self.prompt = prompt
        self.buf = []
        self.pos = 0

    def input(self, key):
        if key == 0x80: # del
            if self.pos == 0:
                return
            self.pos -= 1
            del self.buf[self.pos]
            return

        if key == 6:
            char = ' '
        else:
            char = chr(key)

        self.buf.append(char)
        self.pos += 1

    def str(self):
        return ''.join(self.buf)

    def str_with_prompt(self):
        s = ''.join(self.buf[0:self.pos]) + '|' + ''.join(self.buf[self.pos:])
        return self.prompt + s


class PopupWin(Popup):
    def __init__(self, lines, title = '',
            time = None,
            close = False):
        opt = {}
        opt['minheight']       = 20
        opt['minwidth']        = 75
        opt['maxheight']       = 20
        opt['maxwidth']        = 75
        opt['title']     = title
        opt['border']    = [1, 1, 1, 1]
        opt['drag']      = True
        opt['wrap']            = True

        if time:
            opt['time'] = time
        if close:
            opt['close'] = close

        self.create(lines, opt)


class PopupDialog(Popup):
    def __init__(self, title = ''):
        opt = {}
        opt['minheight'] = 15
        opt['minwidth']  = 50
        opt['title']     = title
        opt['border']    = [1, 1, 1, 1]
        opt['filter']      = "wind#popup_filter"
        opt['cursorline']  = 2

        self.create('', opt)


class PopupSearch(Popup):
    def __init__(self, filter_cb, finish_cb,
            title = 'Popup Search Win',
            center = False):

        self.line = Line(prompt = 'Search> ')
        self.finish_cb = finish_cb
        self.filter_cb = filter_cb
        self.focus_line_nu = 0

        opt = {}
        opt['minheight']       = 20
        opt['minwidth']        = 75
        opt['maxheight']       = 20
        opt['maxwidth']        = 75
        opt['title']           = title
        opt['border']          = [1, 1, 1, 1]
        opt['padding']         = [0, 1, 1, 1]
        opt['filter']          = "wind#popup_filter"
        opt['wrap']            = False
        opt['scrollbar']       = 0
        opt['mapping']         = False
        opt['cursorline']         = True

        if not center:
            opt['line']            = 'cursor+1'
            opt['col']             = 'cursor+1'
            opt['pos']             = 'topleft'

        opt['borderhighlight'] = ['MoreMsg']

        self.create('', opt)
        self.update()

    def update(self, refresh = True):
        if refresh:
            s = self.line.str().split()


            cmd = 'silent! syntax clear PopupKey'
            self.command(cmd)

            for w in s:
                cmd = 'syntax match PopupKey "%s"' %w
                self.command(cmd)

            self.command("hi link PopupKey Type")

            lines = self.filter_cb(s, [])
            self.lines = lines
        else:
            lines = self.lines


        o = []
        o.append(self.line.str_with_prompt())
        o.append('')

        if self.focus_line_nu >= len(lines):
            if len(lines):
                self.focus_line_nu = self.focus_line_nu % len(lines)
            else:
                self.focus_line_nu = 0

        for i, line in enumerate(lines):
            if line[-1] == '\n':
                line = line[0:-1]

            if i == self.focus_line_nu % len(line):
                line = '> %s' % (line, )
            else:
                line = '  %s' % (line, )
            o.append(line)


        self.settext(o)
        self.setpos(self.focus_line_nu + 3)

        return o

    def handle(self, key):
        if key == 9: # \t
            self.focus_line_nu += 1
            self.update(False)
            return

        if key == 13: # cr
            self.close()
            self.finish_cb(self.focus_line_nu)
            return

        if key == 0x1B: # <esc>
            self.close()
            self.finish_cb(-1)
            return

        self.focus_line_nu = 0
        self.line.input(key)
        self.update()



































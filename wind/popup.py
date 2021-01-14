# -*- coding:utf-8 -*-

import vim
from pyvim import log
import pyvim
import subprocess
import time

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
    def create(self, what, op, title = '', filetype = None):
        opt = {}
        if op == None:
            op = {}

        opt['minheight']  = 20
        opt['minwidth']   = 75
        opt['maxheight']  = 20
        opt['maxwidth']   = 75

        opt['title']      = title
        opt['border']     = [1, 1, 1, 1]
        opt['padding']    = [0, 1, 1, 1]
        opt['wrap']       = False
        opt['scrollbar']  = 0

        opt['moved']      = 'any'

        opt['mapping']    = False
        opt['drag']       = True

        opt['filter'] = "wind#popup_filter"

        if not op.get('center'):
            opt['line'] = 'cursor+1'
            opt['col']  = 'cursor+1'
            opt['pos']  = 'topleft'

        opt['borderhighlight'] = ['StatusLine', 'VertSplit', 'VertSplit', 'VertSplit']
        opt['borderchars'] = [' ']

        opt.update(op)
        _ = opt
        opt = {}

        for k, v in _.items():
            if v != None:
                opt[k] =v

        opt['cursorline']  = True # must this for scroll

        if isinstance(what, str):
            what = what.split('\n')

        self.winid = popup.create(what, opt)
        self.bufid = vim.eval('winbufnr(%s)' % self.winid)

        popup.winids[self.winid] = self

        vimfun.setwinvar(self.winid, '&wincolor', 'Normal')

        if filetype:
            cmd = 'call setbufvar(winbufnr(%s), "&filetype", "%s")' % (self.winid, filetype)
            vim.command(cmd)

        self.cursorline = op.get('cursorline')

        if not self.cursorline:
            # popup cursorline use the hi PmenuSel
            cmd = 'hi PmenuSel guifg=NONE guibg=NONE gui=underline ctermfg=NONE ctermbg=NONE cterm=NONE'
            self.command(cmd)
            cmd = 'hi def link PopupCursor CursorColumn'
            self.command(cmd)

        self.offset = 1
        self.focus_line_nu = 0
        self.mode_insert = False
        self.mode_insert_allow = False
        self.ret_bool = False
        self.finish_cb = None
        self.cr_handler = self.finish
        self.finish_cb_arg = None

        # any input as quit
        self.any_close = False

        self.lines = what
        self.hotmaps = {}



    def command(self, cmd):
        vimfun.win_execute(self.winid, cmd)

    def setpos(self, line, col = 0):
        if not self.cursorline:
            cmd = 'silent! syntax clear PopupCursor'
            self.command(cmd)
            cmd = 'syntax match PopupCursor "\\%%%dl^."' % line
            self.command(cmd)

        self.command("call setpos('.', [0, %s, %s,0])"% (line, col))

    def close(self):
        popup.close(self.winid)

    def settext(self, text):
        popup.settext(self.winid, text)

    def setoptions(self, opt):
        popup.setoptions(self.winid, opt)

    def move_cursor(self, off):
        self.focus_line_nu += off

        if self.focus_line_nu > len(self.lines):
            if len(self.lines):
                self.focus_line_nu = self.focus_line_nu % len(self.lines)
            else:
                self.focus_line_nu = 0
        self.setpos(self.focus_line_nu + self.offset)

    def finish(self, status):
        if self.ret_bool:
            i = status
        else:
            if status:
                i = self.focus_line_nu
            else:
                i = -1

        if self.finish_cb:
            if self.finish_cb_arg:
                self.finish_cb(i, self.finish_cb_arg)
            else:
                self.finish_cb(i)

    def handle(self, key):
        if self.any_close:
            self.close()
            self.finish(False)
            return

        if key == 9: # \t
            self.mode_insert = False
            self.update(1, False)
            return

        if key == 13: # cr
            self.close()
            self.finish(True)
            return

        if key == 0x1B: # <esc>
            self.close()
            self.finish(False)
            return

        if not self.mode_insert:
            if key == ord('q'):
                self.close()
                self.finish(False)
                return

            if key == ord('j'):
                self.move_cursor(1)
                return

            if key == ord('k'):
                self.move_cursor(-1)
                return

            if key == 32: # space
                self.move_cursor(5)
                return

            if key == ord('i'):
                if not self.mode_insert_allow:
                    return
                self.mode_insert = True
                self.update(0, False)
                return

            return

        self.line.input(key)
        self.focus_line_nu = 0
        self.update(0)


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
    def __init__(self, lines, title = '', any_close = False, **popup_opt):
        self.create(lines, popup_opt, title = title)
        if any_close: # first for trans
            self.any_close = True

class PopupDialog(Popup):
    def __init__(self, msg, finish_cb = None, arg = None, **popup_opt):
        popup_opt['center'] = True
        popup_opt['cursorline'] = True
        self.create(msg, popup_opt)

        self.finish_cb = finish_cb
        self.finish_cb_arg = arg
        self.ret_bool = True

class PopupRun(Popup):
    def __init__(self, fun, arg = None, finish_cb = None, title = "Popup Run", **popup_opt):
        self.buf = []

        if isinstance(fun, str):
            self.run(fun)
        else:
            fun(self, arg)

        popup_opt['center'] = True
        popup_opt['cursorline'] = True

        self.create(self.buf, popup_opt, title = title)
        self.command("ColorHighlight")

        self.finish_cb = finish_cb
        self.ret_bool = True

    def run(self, cmd, stdin = None):
        if isinstance(cmd, str):
            self.append("$ " + cmd)
        else:
            self.append("$ " + ' '.join(cmd))


        p = subprocess.run(cmd, shell = True,
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT, text = True)

        if stdin:
            p = subprocess.Popen(cmd,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT)
            out,err = p.communicate(stdin)
            self.buf.extend(out.decode('utf8').split('\n'))
        else:
            p = subprocess.run(cmd, shell = True,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT, text = True)
            if p.stdout:
                self.buf.extend(p.stdout.split('\n'))


        return p.returncode

    def append(self, line):
        self.buf.append(line)


class PopupSystem(Popup):
    def __init__(self, cmd, **popup_opt):
        self.lines = ['$ ' + cmd]

        self.create(self.lines, popup_opt, title = cmd)

        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE, shell = True)
        while p.poll() == None:
            o, e = p.communicate()
            if not o:
                time.sleep(0.1)
                continue

            lines = o.split('\n')
            self.lines.extend(lines)
            self.settext(self.lines)

class PopupSelect(Popup):
    def __init__(self, sel, finish_cb, target = None, title = 'Popup Select', **popup_opt):

        popup_opt['cursorline'] = True
        popup_opt['center'] = True

        h = min(20, len(sel) + 2)
        popup_opt['minheight']  = h
        popup_opt['maxheight']  = h

        self.create(sel, popup_opt, title = title)

        self.finish_cb = finish_cb

        if target:
            for i, l in enumerate(sel):
                if l.find(target) > -1:
                    self.move_cursor(i)
                    break

class PopupMenu(PopupSelect):
    def __init__(self, menu, finish_cb, title = 'Popup Menu'):
        PopupSelect.__init__(self, menu, finish_cb, minwidth = 45, maxwidth = 45)


class PopupSearch(Popup):
    def __init__(self, filter_cb, finish_cb, title = 'Popup Search',
            filetype = None,
            **popup_opt):
        popup_opt['cursorline'] = True

        self.create('', popup_opt, title = title, filetype = filetype)

        self.line      = Line(prompt = 'Search> ')
        self.finish_cb = finish_cb
        self.filter_cb = filter_cb
        self.offset    = 3

        self.mode_insert   = True
        self.mode_insert_allow = True

        self.update(0)

        cmd = 'syn keyword Label Search'
        self.command(cmd)
        cmd = "syn match WildMenu '^> '"
        self.command(cmd)

    def update(self, off, refresh = True):
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
        if self.mode_insert:
            o.append(self.line.str_with_prompt())
        else:
            o.append(self.line.str())
        o.append('')


        for i, line in enumerate(lines):
            if line[-1] == '\n':
                line = line[0:-1]

            line = '  %s' % (line, )
            o.append(line)

        self.settext(o)
        self.move_cursor(off)

        return o



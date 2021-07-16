# -*- coding:utf-8 -*-

import vim
from pyvim import log
import pyvim
import subprocess
import time
import sys

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
    def ops(self, op, title):
        opt = {}
        if op == None:
            op = {}

        opt['minheight']  = 20
        opt['minwidth']   = 75
        opt['maxheight']  = 20
        opt['maxwidth']   = 75

        opt['title']      = title
        opt['border']     = [1, 1, 1, 1]
        opt['padding']    = [0, 0, 0, 0]
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

        self.cursorline = op.get('cursorline')
        if self.cursorline:
            self.fake_curosr = False # fake cursor line for line number
        else:
            self.fake_curosr = True # fake cursor line for line number

        return opt

    def init_cursor(self):
        self.back_hi_pmenusel = None
        self.back_hi_pmenucursor = None

        if self.fake_curosr:
            self.back_hi_pmenusel = vim.eval("execute('hi PmenuSel')")
            self.back_hi_pmenusel = vim.eval("execute('hi PopupCursor')")

            # popup cursorline use the hi PmenuSel
            cmd = 'hi! link PmenuSel Normal'
            self.command(cmd)
            cmd = 'hi! link PopupCursor CursorColumn'
            self.command(cmd)

        else:
            self.back_hi_pmenusel = vim.eval("execute('hi PmenuSel')")

            cmd = 'hi! link PmenuSel CursorLine'
            self.command(cmd)

    def reset_hi(self):
        if self.back_hi_pmenusel:
            o = self.back_hi_pmenusel.split()[2:]
            cmd = "hi PmenuSel " + ' '.join(o)
            vim.command(cmd)

        if self.back_hi_pmenucursor:
            o = self.back_hi_pmenucursor.split()[2:]
            cmd = "hi PopupCursor " + ' '.join(o)
            vim.command(cmd)


    def init_buf(self, filetype, linenu):
        vimfun.setwinvar(self.winid, '&wincolor', 'Normal')
        if linenu:
            self.command("set nu")

        if filetype:
            cmd = 'call setbufvar(winbufnr(%s), "&filetype", "%s")' % (self.winid, filetype)
            vim.command(cmd)

    def init_var(self):
        self.bufid = vim.eval('winbufnr(%s)' % self.winid)

        popup.winids[self.winid] = self

        self.offset            = 1
        self.focus_line_nu     = 0
        self.mode_insert       = False
        self.mode_insert_allow = False
        self.ret_bool          = False
        self.finish_cb         = None
        self.cr_handler        = self.finish
        self.finish_cb_arg     = None

        # any input as quit
        self.any_close = False

        self.hotmaps   = {}

    def create(self, what, op, title = '', filetype = None, linenu = True):
        self.winid = popup.create('', self.ops(op, title))

        self.init_var()

        self.settext(what)
        # if show not same with lines, should set line after lines
        self.lines = what

        self.init_buf(filetype, linenu)
        self.init_cursor()

    def command(self, cmd):
        vimfun.win_execute(self.winid, cmd)

    def setpos(self, line, col = 0):
        if self.fake_curosr:
            cmd = 'silent! syntax clear PopupCursor'
            self.command(cmd)
            cmd = 'syntax match PopupCursor "\\%%%dl^."' % line
            self.command(cmd)

        self.command("call setpos('.', [0, %s, %s,0])"% (line, col))

    def close(self):
        popup.close(self.winid)

    def settext(self, what):

        if isinstance(what, str):
            what = what.split('\n')

        if self.fake_curosr:
            for i,l in enumerate(what):
                if l == '':
                    what[i] = ' '

        popup.settext(self.winid, what)

    def setoptions(self, opt):
        popup.setoptions(self.winid, opt)

    def move_cursor(self, off, goto_buttom = False, goto_top = False):
        if goto_buttom and len(self.lines):
            self.focus_line_nu = len(self.lines) - 1
        elif goto_top:
            self.focus_line_nu = 0
        else:
            self.focus_line_nu += off

            if self.focus_line_nu >= len(self.lines):
                self.focus_line_nu = len(self.lines) - 1

            if self.focus_line_nu < 0:
                self.focus_line_nu = 0

        self.setpos(self.focus_line_nu + self.offset)

    def finish(self, status):
        self.close()

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

        self.reset_hi()

    def handle(self, key):
        if self.any_close:
            self.finish(False)
            return

        if key in self.hotmaps:
            self.focus_line_nu = self.hotmaps[key]
            self.finish(True)
            return

        if key == 9: # \t
            self.mode_insert = False
            self.update(1, False)
            return

        if key == 13: # cr
            self.finish(True)
            return

        if key == 0x1B: # <esc>
            self.finish(False)
            return

        if not self.mode_insert:
            if key == ord('q'):
                self.finish(False)
                return

            if key == ord('j'):
                self.move_cursor(1)
                return

            if key == ord('k'):
                self.move_cursor(-1)
                return

            if key == ord('G'):
                self.move_cursor(1, goto_buttom = True)
                return

            if key == ord('g'):
                self.move_cursor(1, goto_top = True)
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
    def __init__(self, msg, finish_cb = None, arg = None, title = 'Dialog', **popup_opt):
        popup_opt['center'] = True
        popup_opt['cursorline'] = False
        self.create(msg, popup_opt, title= title, linenu = False)

        self.finish_cb = finish_cb
        self.finish_cb_arg = arg
        self.ret_bool = True

class PopupTips(Popup):
    def __init__(self, what, title = "Popup Tips", **popup_opt):
        popup_opt['center'] = True
        popup_opt['cursorline'] = False
        popup_opt['wrap'] = False
        popup_opt['filter'] = None
        popup_opt['moved'] = None
        popup_opt['line'] = 1
        popup_opt['col'] = vim.current.window.width
        popup_opt['pos'] = 'topright'
        popup_opt['minheight']  = 10
        popup_opt['minwidth']   = 35
        popup_opt['maxheight']  = 10
        popup_opt['maxwidth']   = 45

        self.create(what, popup_opt, title = title)

class PopupRun(Popup):
    def __init__(self, fun, arg = None, finish_cb = None, title = "Popup Run", **popup_opt):
        self.buf = []

        if isinstance(fun, str):
            self.run(fun)
        elif isinstance(fun, list):
            for s in fun:
                self.run(s)
        else:
            stdout = sys.stdout
            stderr = sys.stderr
            sys.stdout = self
            sys.stderr = self
            try:
                if arg:
                    fun(self, arg)
                else:
                    fun()
            except Exception as e:
                self.append(e)

            sys.stdout = stdout
            sys.stderr = stderr
            self.append("========== END ==========")

        opt = {}
        opt['center'] = True
        opt['cursorline'] = False
        opt['wrap'] = True
        opt['minheight']  = 20
        opt['minwidth']   = 85
        opt['maxheight']  = 20
        opt['maxwidth']   = 85
        opt.update(popup_opt)

        self.create(self.buf, opt, title = title)
        # 支持终端转义 color, Colorizer plugin
        self.command("ColorHighlight")

        self.finish_cb = finish_cb
        self.ret_bool = True

    def run(self, cmd, stdin = None):
        ps1 ="\033[01;35m$ \033[0m"
        if isinstance(cmd, str):
            self.append(ps1 + cmd)
        else:
            self.append(ps1 + ' '.join(cmd))

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

    def append(self, buf):
        if buf[-1] == '\n':
            buf = buf[0:-1]

        lines = buf.split('\n')
        self.buf.extend(lines)

    def write(self, buf): # for stdout
        self.append(buf)


class PopupSystem(Popup):
    def __init__(self, cmd, **popup_opt):
        self.create(self.lines, popup_opt, title = cmd)
        self.lines = ['$ ' + cmd]

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

#        h = min(20, len(sel) + 2)
        h = len(sel) + 2
        if h < 12:
            h = 12
        popup_opt['minheight']  = h
        popup_opt['maxheight']  = h

        self.create(sel, popup_opt, title = title, linenu = False)

        self.finish_cb = finish_cb

        if target:
            for i, l in enumerate(sel):
                if l.find(target) > -1:
                    self.move_cursor(i)
                    break

        cmd = "syn match LineNr '=.*='"
        self.command(cmd)

class PopupMenuItem(object):
    def __init__(self, show, callback = None, arg = None):
        self.show = show
        self.callback = callback
        self.arg = arg

class PopupMenu(PopupSelect):
    def __init__(self, menu, title = 'Popup Menu', hotkey = True):
        self.menu = menu
        show = []

        for m in menu:
            show.append(m.show)

        hotmaps = {}
        for i, l in enumerate(show):
            if hotkey:
                for c in l:
                    c = c.upper()
                    k = ord(c)
                    if k < ord('A') or k > ord('Z'):
                        continue

                    if k not in hotmaps:
                        hotmaps[k] = i
                        show[i] = '%s. %s' % (c, l)
                        break
            else:
                show[i] = '  %s' % (l, )

        PopupSelect.__init__(self, show, self.finish_cb, title = title,
                minwidth = 60, maxwidth = 60)

        self.hotmaps = hotmaps

    def finish_cb(self, i):
        if i < 0:
            return
        m = self.menu[i]
        if m.callback == None:
            return

        m.callback(m.arg)

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
            if line and line[-1] == '\n':
                line = line[0:-1]

            line = '  %s' % (line, )
            o.append(line)

        self.settext(o)
        self.move_cursor(off)

        return o



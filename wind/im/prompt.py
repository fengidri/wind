# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-05 13:01:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os

from plugins import Plugins
from imutils import Redirect
import vim
from pyvim import log
import imrc
import env

_prompt = []
__Handles = {}

class Status(object):
    name = ''

def prompt(name):
    "Decorator set the first handle."
    """
        prompt need two call back handle: findstart, base;

        @name: the prompt handle name

        @findstart:
             return the len of the word before cursor to be replace.
             if the return val < 0 has special. see it by
             `help complete-functions`

             the other val < 0 be used by wind. Such as -4 is used by ycm.
             If the return val == -4, wind will call ycmcompleteme to complete;

        @base:
             return the list of the match item.
             But, you shuld use the prompt.abuild to build the complete item.
    """
    def _fun(findstart):
        def xx(base):
            __Handles[name] = (findstart, base)
            return base
        return xx
    return _fun

def Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'prompt')

    plugins = Plugins(ftpath)
    plugins.loads()
    log.error(__Handles)


class NotPrompt(Exception):
    pass




################################################################################
def append_string(ppt):
    _prompt.append({"word": ppt})

def append_list(ppt):
    for x in ppt:
        if isinstance(x, dict):
            _prompt.append(x)

        elif isinstance(x, basestring):
            append_string(x)



def append(ppt):
    if isinstance(ppt, list):
        append_list(ppt)

    elif isinstance(ppt, basestring):
        append_string(ppt)

def build(word, abbr = None, menu = None):
    s = {"word": word}
    if abbr:
        s["abbr"] = abbr

    if menu:
        s["menu"] = menu

    return s

def abuild(word, abbr = None, menu = None):
    _prompt.append(build(word, abbr, menu))

################################################################################

def popmenu():
    if not _prompt:
        return
    vim.vars["omniresult"] = _prompt
    vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1



def active():
    func = "wind#Prompt"
    vim.command("let &omnifunc='%s'" % func)
    vim.command("let &l:omnifunc='%s'" % func)
    #imrc.feedkeys('\<C-X>\<C-O>\<C-P>')
    imrc.feedkeys('\<C-X>\<C-O>')
    return True

def findstart():
    tt = None
    col = -3

    handle_list = Redirect().getcur('prompt')
    log.debug('findstart hande list: %s', handle_list )
    for hd in handle_list:
        tt = __Handles.get(hd)
        if not tt:
            continue

        try:
            col = tt[0]()
            if not isinstance(col, int):
                col = -3
        except NotPrompt:
            col = -3

        if col > -1:
            log.error('@findstart redirect: %s' % hd)
            Status.name = hd
            _col = env.col - col
            log.error("find start: %s %s %s", _col, col, env.col)
            return _col
    return col

def Base(base):
    hd = __Handles.get(Status.name)[1]
    if not hd:
        return []

    del _prompt[:]
    hd(base)
    return _prompt


def handle(event, base=None):

    if event == 'done':
        Status.findstart = None
        Status.base = None
        Status.name = ''
        return

    #if __handle[0] == None or __handle[1] == None:
    #    vim.vars["omnicol"] = -3
    #    vim.vars["omniresult"] = []
    #    return

    if event == "findstart":
        vim.vars["omnicol"] = findstart()

    elif event == "base":
        vim.vars["omniresult"] = {'words':Base(base), 'refresh': 'always'}

if __name__ == "__main__":
    pass


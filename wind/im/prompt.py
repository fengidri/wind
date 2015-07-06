# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-05 13:01:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

"""
   prompt 用于进行输入提示.
   1. 外部调用
        由外部程序完成补全功能. wind 只是负责 prompt 的调用与 pop 菜单的处理.
        在 pop 菜单出现的情况下, 所做的事情也只有 <tab> 对于 item 的选择.

   2. 内部调用
   2.1 no session
       这种情况与外部的调用相似, 也是没有 session 的. 在 pop 菜单出现的情况
       也就是完成 <tab> 的行为.

       由 wind 完成 prompt item 的生成. 但是由于没有 session, 所以 prompt 不会
       代理这个过程

       例如: path prompt.

   2.2 session
       目前只用于 wubi. 这种的行为是比较复杂的, prompt 还要代理 prompt item 的生
       成.



"""
_prompt = []
__handle = [None, None]
from pyvim import log
import vim
import imrc

def init(handle, h):
    __handle[0] = handle
    __handle[1] = h

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


def popmenu():
    if not _prompt:
        return
    vim.vars["omniresult"] = _prompt
    vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1



def active():
    func = "wind#Prompt"
    vim.command("let &omnifunc='%s'" % func)
    vim.command("let &l:omnifunc='%s'" % func)
    imrc.feedkeys('\<C-X>\<C-O>\<C-P>')
    return True




def handle(event, base=None):

    #if event == 'done':
    #    __handle[0] = None
    #    __handle[1] = None
    #    return

    #if __handle[0] == None or __handle[1] == None:
    #    vim.vars["omnicol"] = -3
    #    vim.vars["omniresult"] = []
    #    return

    if event == "findstart":
        try:
            col = __handle[0]()
            if not isinstance(col, int):
                col = -3
        except NotPrompt:
            col = -3
        vim.vars["omnicol"] = col
        return

    elif event == "base":
        global _prompt
        #del _prompt[:]
        _prompt = []
        __handle[1](base)
        log.error('_prompt: %s', len(_prompt))
        vim.vars["omniresult"] = {'words':_prompt, 'refresh': 'always'}
        return

if __name__ == "__main__":
    pass


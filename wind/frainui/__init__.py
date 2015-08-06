# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:15:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from node import Node, Leaf
from listwin import LIST
from searchwin import Search
from pyvim import log
import utils
import vim

def inputstream(tp, key):
    # 处理从 IM Stream 过来的输入流
    # 输入流必然会进入 Buffer 对象
    obj = utils.Objects.get(vim.current.buffer)
    if not obj:
        return

    widget = obj.input_focus
    if widget and widget.IM:
        getattr(widget.IM, tp)(key)


def handle(ev, name = None):
    #处理由 IM 触发的事件
    # 在不指定 name 的情况下, 会把事件传递给当前的 buffer
    # 所以多大情况下, 在 Buffer 对象会是 widget 的事件代理.

    if not name:
        name = vim.current.buffer
    log.debug(utils.Objects)

    obj = utils.Objects.get(name)
    if not obj:
        return

    # 由 IM 触发 object 的事件
    obj.FREventEmit(ev)


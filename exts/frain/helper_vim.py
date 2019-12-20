# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-01-26 08:42:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os

import utils
import project

import vim
import pyvim
from pyvim import log

def BufEnter(FrainList):
    # this is '' inside python3
    #if vim.current.buffer.options[ 'buftype' ] != '':
    #    return -1

    if vim.current.buffer.name == '':
        return -1

    """显示当前的 buffer 对应的文件在 win list 中的位置
    如果, buffer 不属于任何一个 project, 返回 `NROOT'
    之后生成当前 buffer 在 win list 中的 url, 由 win list 进行查询.
    """
    path = utils.bufferpath()
    if not path:
        return
    log.info('path: %s', path)

    for p in project.Project.All:
        if path.startswith(p.root):
            break
    else:
        return

    names = utils.getnames(p.root, path)
    FrainList.listwin.find(names)


def BufNewFile(FrainList):
    path = vim.current.buffer.name

    if vim.current.buffer.options['buftype'] != '':
        return

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)

    if FrainList.new_files.get(dirname):
        FrainList.new_files.get(dirname).append(basename)
    else:
        FrainList.new_files[dirname] = [basename]

def BufNew(FrainList):
    if FrainList.buf_node:
        FrainList.buf_node.refresh()

def VimLeave(FrainList):
    project.Project.emit("FrainLeave")

    if FrainList.origin_window_title:
        pyvim.settitle(FrainList.origin_window_title)



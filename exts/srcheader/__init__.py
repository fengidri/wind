#encoding:utf8
import pyvim
import vim
import time
import os

def get_desc():
    ft = vim.eval("&ft")
    fts = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fts')

    path = os.path.join(fts, ft)
    if not os.path.isfile(path):
        return
    return open(path).readlines()

@pyvim.event("FileType")
def run():
    if pyvim.is_empty():
        add_src_info()

@pyvim.cmd()
def SrcInfoAdd():
    add_src_info()

def add_src_info():
    lines = get_desc()
    if not lines:
        return

    ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    author = vim.vars.get("wind_author")
    email  = vim.vars.get("wind_email")

    ch_name = vim.current.buffer.name
    ch_name = os.path.basename(ch_name)
    ch_name = ch_name.upper()
    ch_name = ch_name.replace('.', '_')
    ch_name = ch_name.replace(' ', '_')
    ch_name = ch_name.replace('-', '_')

    index = 0
    for l in lines:
        l = l.format(time=ntime, ch_name=ch_name, author=author, email=email)
        vim.current.buffer.append(l, index)
        index += 1


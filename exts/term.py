# -*- coding:utf-8 -*-



import os
import pyvim
import vim
import subprocess


@pyvim.cmd()
def TmuxPopupTerm():
    cmd = ['tmux', 'popup', '-E', '-K', '-R', 'zsh', '-d']

    root = pyvim.get_cur_root()
    if root:
        cmd.append(root)
    else:
        cmd.append(os.path.dirname(vim.current.buffer.name))

    subprocess.Popen(cmd)


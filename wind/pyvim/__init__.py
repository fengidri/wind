# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:47:53
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
"""
Pyvim is a lib for ext and other modules.
"""

class complete(object):
    augroup       = "augroup"               # autocmd groups
    buffer        = "buffer"                # buffer names
    behave        = "behave"                # :behave suboptions
    color         = "color"                 # color schemes
    command       = "command"               # Ex command (and arguments)
    compiler      = "compiler"              # compilers
    cscope        = "cscope"                # |:cscope| suboptions
    dir           = "dir"                   # directory names
    environment   = "environment"           # environment variable names
    event         = "event"                 # autocommand events
    expression    = "expression"            # Vim expression
    file          = "file"                  # file and directory names
    file_in_path  = "file_in_path"          # file and directory names in |'path'|
    filetype      = "filetype"              # filetype names |'filetype'|
    function      = "function"              # function name
    help          = "help"                  # help subjects
    highlight     = "highlight"             # highlight groups
    history       = "history"               # :history suboptions
    locale        = "locale"                # locale names (as output of locale -a)
    mapping       = "mapping"               # mapping name
    menu          = "menu"                  # menus
    option        = "option"                # options
    shellcmd      = "shellcmd"              # Shell command
    sign          = "sign"                  # |:sign| suboptions
    syntax        = "syntax"                # syntax file names |'syntax'|
    syntime       = "syntime"               # |:syntime| suboptions
    tag           = "tag"                   # tags
    tag_listfiles = "tag_listfiles"         # tags, file names are shown when CTRL-D is hit
    user          = "user"                  # user names
    var           = "var"                   # user variables

from pyvim import *
from event import *
from cmd import *



if __name__ == "__main__":
    pass


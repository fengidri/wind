#encoding:utf8
import pyvim
import vim
import time
import os
author = "陈小雪"
email = "shell_chen@yeah.net"
_infos = """
>sh
#!/usr/bin/env sh
#    author    :   {author}
#    time      :   {time}
#    email     :   {email}
#    version   :   1.0.1

>python
# -*- coding:utf-8 -*-
#    author    :   {author}
#    time      :   {time}
#    email     :   {email}
#    version   :   1.0.1


if __name__ == "__main__":
    pass

>js
/**
 *   author       :   {author}
 *   time         :   {time}
 *   email        :   {email}
 *   version      :   1.0.1
 *   description  :
**/

>c
/**
 *   author       :   {author}
 *   time         :   {time}
 *   email        :   {email}
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>

>lua
--
-- author       :   {author}
-- time         :   {time}
-- email        :   {email}
-- version      :   1.0.1
-- description  :
--

>cpp
/**
 *   author       :   {author}
 *   time         :   {time}
 *   email        :   {email}
 *   version      :   1.0.1
 *   description  :
 */

>ch
/**
 *   author       :   {author}
 *   time         :   {time}
 *   email        :   {email}
 *   version      :   1.0.1
 *   description  :
 */
#ifndef  __{ch_name}__
#define __{ch_name}__

#endif
"""
infos= None
def get_infos():
    tmp = {}
    tl = _infos.split("\n>")
    for context in tl:
        lines = context.split('\n')
        info = lines[1:]
        for ft in lines[0].split(','):
            tmp[ft] = info
    return tmp


@pyvim.event("FileType")
def run():
    if pyvim.is_empty():
        add_src_info()

@pyvim.cmd()
def SrcInfoAdd():
    aasctimedd_src_info()



def add_src_info():
    global infos
    ft = vim.eval("&ft")
    if not infos:
        infos = get_infos()
    info = infos.get(ft)
    if not info:
        return
    ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() )

    ch_name = vim.current.buffer.name
    ch_name = os.path.basename(ch_name)
    ch_name = ch_name.upper()
    ch_name = ch_name.replace('.', '_')
    ch_name = ch_name.replace(' ', '_')
    ch_name = ch_name.replace('-', '_')

    index = 0
    for l in info:
        l = l.format(time = ntime,
                ch_name=ch_name,
                author=author,
                email = email)
        vim.current.buffer.append(l, index)
        index += 1


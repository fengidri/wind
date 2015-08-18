# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim

@pyvim.cmd()
def Align(tag = ' '):
        pos1, pos2 = pyvim.selectpos()
        line1 = pos1[0]
        line2 = pos2[0] + 1
        lines = vim.current.buffer[line1: line2]

        if tag == ' ':
            lines = align_fun(lines)
        else:
            lines = align_fun_with_tag(lines, tag)

        vim.current.buffer[line1: line2] = lines

def align_fun_with_tag(lines, tag):
    lines = [line.split(tag) for line in lines]

    lines = align(lines)

    join_tag = " " + tag + ' '
    return [join_tag.join(line).rstrip() for line in lines]

def align_fun(lines, tag = ' '):
    lines = [align_split(line) for line in lines]

    lines = align(lines)

    return [' '.join(line).rstrip() for line in lines]

def align(lines):
    max_len = 0
    for line in lines:
        max_len = max(max_len, len(line))

    max_len_list = [0] * max_len
    for line in lines:
        for i, w in enumerate(line):
            max_len_list[i] = max(max_len_list[i], len(w))
    for line in lines:
        for i, w in enumerate(line):
            if i == 0:
                line[i] = w.rstrip().ljust(max_len_list[i])
            else:
                line[i] = w.strip().ljust(max_len_list[i])
    return lines



def align_split(line):
    start = 1
    split_list = []
    buf = []
    for i in line:
        if start ==  1:
            buf.append(i)
            if not(i in '\t '):
                start = 0
        else:
            if i in '\t ':
                if len(buf) >0:
                    split_list.append(''.join(buf))
                    del buf[:]
            else:
                buf.append(i)
    if len(buf) >0:
        split_list.append(''.join(buf))
        del buf[:]
    return split_list




# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim

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

def ignore_word(line):
    iws = ['const', 'unsigned', 'struct']

    prefix = []

    i = 0
    while i < len(line):
        w = line[i]
        prefix.append(w)
        if w not in iws:
            break
        i += 1

    if not i:
        return line

    if i + 1 < len(line):
        line = line[i+1:]
    else:
        line = []
    line.insert(0, ' '.join(prefix))
    pyvim.log.error(line)
    pyvim.log.error(prefix)
    return line


@pyvim.cmd()
def Align(tag = ' '):
        pos1, pos2 = pyvim.selectpos()
        line1 = pos1[0]
        line2 = pos2[0] + 1
        lines = vim.current.buffer[line1: line2]

        space_before = 0
        for i in lines[0]:
            if i == ' ':
                space_before += 1
            elif i == '\t':
                space_before += 4
            else:
                break
        space_before = ' ' * space_before

        lines = [line.split(tag) for line in lines]
        for i, line in enumerate(lines):
            line = [t.strip() for t in line]
            line = [t for t in line if t]
            lines[i] = ignore_word(line)

        lines = align(lines)

        if ' ' == tag:
            join_tag = tag
        else:
            join_tag = " " + tag + ' '



        vim.current.buffer[line1: line2] = \
                [space_before + join_tag.join(line).rstrip() for line in lines]




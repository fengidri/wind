import pyvim
import vim
class Align( pyvim.command ):
    def run( self ):
        start = int(vim.eval("line(\"'<\")"))
        end   = int(vim.eval("line(\"'>\")"))
        lines = vim.current.buffer[start - 1: end]
        lines = align_fun(lines)
        vim.current.buffer[start - 1:end] = lines

class AlignTag( pyvim.command ):
    def run( self ):
        if self.params:
            tag = self.params[ 0 ]
        else:
            tag = "//"
        start = int(vim.eval("line(\"'<\")"))
        end   = int(vim.eval("line(\"'>\")"))
        lines = vim.current.buffer[start - 1: end]
        lines = align_fun_with_tag(lines, tag)
        vim.current.buffer[start - 1:end] = lines


def align_fun_with_tag( lines, tag ):
    lines = [line.split(tag) for line in lines]
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
    join_tag = " " + tag + ' '
    lines = [join_tag.join(line).rstrip() for line in lines]
    return lines

def align_fun(lines, tag = ' '):
    lines = [align_split(line) for line in lines]
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
    lines = [' '.join(line).rstrip() for line in lines]
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

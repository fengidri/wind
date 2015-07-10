# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-19 14:28:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import re

import vim
from pyvim import log as logging
import im.prompt as prompt
import im.env as env

ShowUrl = 'http://localhost/autofresh/data'
__regex = re.compile(r"\\[a-zA-Z]+$")
__word = re.compile(r"\\[a-zA-Z]+")


@prompt.prompt("tex")
def tex():
    match = __regex.search(env.before)
    if match:
        return len(match.group())

@tex
def base(base):
    words = []
    for line in vim.current.buffer:
        words += __word.findall(line)

    words = list(set(words))

    prompt.append_list(words)


if __name__ == "__main__":
    pass


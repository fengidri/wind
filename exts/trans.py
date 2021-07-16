# -*- coding:utf-8 -*-


import vim
from bs4 import BeautifulSoup

import pyvim
import requests
import json

import popup
import os

def translate_google(text):
    #https://github.com/soimort/translate-shell
    cmd = "trans -brief '%s' 2>/dev/null" % text
    return os.popen(cmd).read()


def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        result = json.loads(response.text)
        result = result['translateResult'][0][0]['tgt']
        return result
    else:
        # 相应失败就返回空
        return None

def dict_en(w):
    url = 'http://www.youdao.com/w/'
    r = url + w
    r = requests.get(r)
    if r.status_code != 200:
        return ['Request Fail']

    soup = BeautifulSoup(r.text, features="html.parser")
    ret = soup.findAll('div', attrs={'class': 'trans-container'})
    if not ret:
        return ['Request Fail']

    ret = ret[0].findNext('ul').text
    return ret.split('\n')


"""
    ===========================================================================
"""

"""
    return text,  last linenu
"""
def current_text():
    linenu = vim.current.window.cursor[0] - 1

    lines = []

    while True:
        if linenu >= len(vim.current.buffer):
            break

        line = vim.current.buffer[linenu]
        linenu += 1
        line = line.strip()
        if not line:
            break

        lines.append(line)

    text = ' '.join(lines)
    return text, linenu

def __translines(yd = True):
    text, linenu = current_text()

    if yd:
        result = translate(text)
    else:
        result = translate_google(text)

    vim.current.buffer.append(result, linenu - 1)
    vim.current.window.cursor = (linenu, 0)
    vim.command('normal Vgq')

@pyvim.cmd()
def Translate(yd = None):
    __translines(yd)

class g:
    lastwin = None
    lines = []
    last = None


def trans(word):
    list_trans = translate(word)

    if not list_trans:
        return None

    return list_trans



def show():
    if g.lastwin:
        g.lastwin.close()
        g.lastwin = None

    w = popup.PopupWin(g.lines, title="Wind Trans", any_close = True, maxwidth=40)

    g.lastwin = w

def format(word, ret):
    line = []
    line.append(" %s:" % word)

    for r in ret:
        r = r.strip()
        if not r:
            continue

        t = r.split('.', 1)
        if len(t) == 2:
            prefix = t[0] + '.'
            r = t[1]
        else:
            prefix = ''
            r = r[0]

        ind = 5
        for i, x in enumerate(r.strip().split('；')):
            if i != 0:
                indent = ' ' * ind
            else:
                indent = prefix.ljust(ind)

            line.append("   " + indent + x)
    return line

def trans_handle(word):
    if word.find(' ') > -1:
        ret = [trans(word)]
    else:
        ret = dict_en(word)

    line = format(word, ret)

    if g.lines:
        line.append('')
        line.append("------------")
        line.extend(g.lines)

    g.lines = line

def __trans(word):
    word = word.replace('\n', ' ')
    if word != g.last:
        g.last = word
        trans_handle(word)

    show()


@pyvim.cmd()
def Dict(word = None):
    if word == None:
        word = pyvim.current_word()

    __trans(word)

@pyvim.cmd()
def DictV():
    __trans(pyvim.select())

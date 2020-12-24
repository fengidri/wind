# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup

import pyvim
import requests
import json

import popup

class g:
    lastwin = None
    lines = []
    last = None

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
        return response.text
    else:
        # 相应失败就返回空
        return None


def trans(word):
    list_trans = translate(word)

    if not list_trans:
        return None

    result = json.loads(list_trans)
    result = result['translateResult'][0][0]['tgt']
    return result



url = 'http://www.youdao.com/w/'

def dict_en(w):
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

def __trans(word):
    word = word.replace('\n', ' ')
    if word == g.last:
        return

    g.last = word

    if word.find(' ') > -1:
        ret = [trans(word)]
    else:
        ret = dict_en(word)

    line = []
    line.append(" %s:" % word)
    for r in ret:
        r = r.strip()
        if not r:
            continue

        index = r.find('.')
        if index > 0:
            index = index + 2
        else:
            index = 0

        for i, x in enumerate(r.split('；')):
            if i != 0:
                indent = ' ' * index
            else:
                indent = ''
            line.append("   " + indent + x)


    if g.lines:
        line.append('')
        line.append("------------")
        line.extend(g.lines)

    g.lines = line

    if g.lastwin:
        g.lastwin.close()
        g.lastwin = None

    w = popup.PopupWin(line, title="Wind Trans")

    g.lastwin = w

@pyvim.cmd()
def Trans(word = None):
    if word == None:
        word = pyvim.current_word()

    __trans(word)

@pyvim.cmd()
def TransV():
    __trans(pyvim.select())

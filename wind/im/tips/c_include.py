# -*- coding:utf-8 -*-
#    author    :   b'\xe4\xb8\x81\xe9\x9b\xaa\xe5\xb3\xb0'
#    time      :   2020-02-26 08:28:37
#    email     :   b'fengidri@yeah.net'
#    version   :   1.0.1



import time
import datetime
import im.prompt as prompt
import im.env as env
import os

class Prompt(prompt.Prompt):
    prefix = []
    def findstart(self):
        t = env.before.split(' ', 1)
        if len(t) == 1:
            return

        if t[1][0] != '<':
            return

        self.prefix = t[1][1:].split('/')
        return len(t[1]) - 1


    def base(self, base):
        path = include = '/usr/include/'

        for m in self.prefix[0:-1]:
            path = os.path.join(path, m)

        prefix = self.prefix[-1]
        fs = os.listdir(path)

        for f in fs:
            if f.startswith(prefix):
                word = os.path.join(path, f)[len(include):]
                self.abuild(word, abbr = f)



p = Prompt()

def handler():
    if env.ft not in ['c', 'h', 'cpp']:
        return

    if env.before.startswith('#include <'):
        p.active()
        return True


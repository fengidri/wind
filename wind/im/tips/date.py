# -*- coding:utf-8 -*-
#    author    :   b'\xe4\xb8\x81\xe9\x9b\xaa\xe5\xb3\xb0'
#    time      :   2020-02-25 17:37:55
#    email     :   b'fengidri@yeah.net'
#    version   :   1.0.1

import time
import datetime
import im.prompt as prompt
import im.env as env

class Prompt(prompt.Prompt):
    def findstart(self):
        return 4

    def base(self, base):
        self.abuild(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.abuild(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.abuild(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.abuild('%s' % time.time())
        self.abuild('%s' % int(time.time()))
        self.abuild(datetime.datetime.now().isoformat())



p = Prompt()

def handler():
    if env.before.endswith('date'):
        p.active()
        return True

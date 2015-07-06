# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 17:59:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from im.keybase import BasePass
from im.imrc import feedkeys

class IM_Prompt(BasePass):
    def cb_tab(self):
        feedkeys('\<C-n>')
        return True

    def cb_enter(self):
        feedkeys('\<C-e>')
        return True

    def cb_esc(self):
        feedkeys('\<esc>')
        return True

    def cb_space(self):
        feedkeys('\<C-N>')
        feedkeys('\<C-Y>')
        return True

    def cb_backspace(self):
        feedkeys('\<bs>')
        feedkeys('\<C-X>\<C-O>\<C-P>')  # TODO   should auto
        return True


if __name__ == "__main__":
    pass


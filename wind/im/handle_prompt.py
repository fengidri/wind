# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-29 17:58:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import im.imrc
from im.imrc     import feedkeys
from imutils     import add_hook
from handle_base import IM_Base
import env
import imutils

__handle = None
__follow_mode = True # 跟随模式
__show_prompt = False



handle = None


@imutils.hook('start')
def start():
    global __show_prompt
    __show_prompt = False

@imutils.hook('pre-stop')
def stop():
    global __show_prompt
    if __show_prompt:
        feedkeys('\<C-X>\<C-O>')
        __show_prompt = False



class IM_Prompt(IM_Base):
    def active(self):
        handle = None

    def cb_tab(self):
        feedkeys('\<C-n>')
        return True

    def cb_enter(self):
        feedkeys('\<C-e>')
        return True

    def cb_esc(self):
        imrc.feedkeys('\<esc>')
        return True


    #def im_digit(self, key):
    #    word = self.pmenu.getselect(int(key)).get('word')
    #    feedkeys(word)
    #    return True
if __name__ == "__main__":
    pass


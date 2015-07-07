# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 18:05:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from im.keybase import BasePass
import im.imrc as imrc

import im.prompt as prompt
class IM_ActivePrompt(BasePass):
    def active(self, key=None):
        prompt.active()
        return True

    cb_underline = active
    cb_dot = active
    im_digit = active
    im_lower = active
    im_upper = active
    cb_backspace = active




if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 17:04:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
"""
    所有的inputers
    由filetype 下的模块选择合适的inputer组成处理方法队列.
"""

from inputer_path import IM_Path
from inputer_base import IM_Base
from inputer_code import IM_Code
from inputer_wubi import IM_Wubi
from inputer_tex  import IM_Tex
from inputer_frainui  import IM_Stream

if __name__ == "__main__":
    pass


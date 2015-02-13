# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-13 19:23:22
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from base_context import Base_Context_Fsm
from path_context import Path_Context_Fsm
contexts = [ 
        Path_Context_Fsm(),
        Base_Context_Fsm() 
        ]
def all_key(): #TODO all_keys 的设计要调整
    return Base_Context_Fsm().all_key()
    

if __name__ == "__main__":
    pass


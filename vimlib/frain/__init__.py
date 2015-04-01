# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:15:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
global __START_LOCK = False

# 开启frain, 参数可以是多个路径(也可以是远程路径
def api_start(root):
    if __START_LOCK: return
    __START_LOCK = True

    #start ...........

def api_addroot(root):
    pass

# 进行刷新, 没有参数
def api_refresh(): 
    pass

# 用于在list 窗口中显示path
def api_find(path):
    pass

# 返回当前的文件所在的root
def cur_root():
    pass

# 回车的回调, 只用于组成命令, 不用于api
def cmd_open():
    pass


if __name__ == "__main__":
    pass


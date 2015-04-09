# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-09-05 16:21:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import mescin
import paths_exp
def frnames():#所有的工程名
        mescin.init( )
        return mescin.Config.get_info_for_select()

def fropen(name):#打开工程
    cfg, runtime = mescin.Config.get_by_name( name )
    if not (cfg and runtime):
        return False, False
    return cfg, runtime

def frfiles():#当前工程中的文件名
    return paths_exp.get_files()

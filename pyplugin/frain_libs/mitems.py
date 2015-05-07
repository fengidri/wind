#encoding:utf8
import vim
from data import settings

import paths_exp
import os
import mescin

def frain_open(  ):
    """
        打开frain 模式:
              在设置好settings 的前提下打开frain 模式
    """
    paths_exp.refresh_nodes( )
    paths_exp.refresh_win( )




################################
# Commands API
################################



    """
        1. frain 已经打开的情况下, 新加一个目录
        2. frain 没有打开的情况下, 打开一个目录, 进入frain 模式
    """
def frain_open_dir( dir_name ):
    if os.path.isdir( dir_name ):
        dir_name = os.path.realpath( dir_name )
        paths = settings[ "paths" ]

        paths.append( { "path": dir_name } )
        frain_open( )


def close( ):
    """
        退出frain 模式
    """
    global settings

    files=[  ]
    for w in vim.windows:
        if w.buffer.options[ 'buftype' ] == '':
            files.append( w.buffer.name )
    files=','.join( files )

    settings[ "last_open" ] = files

    """
        保存当前的数据信息到文件
    """
    mescin.save( settings )


#encoding:utf8

import mitems
import os
import pyvim
import vim
import re
"""
TODO  2014年 12月 08日 星期一 13:38:21 UTC
      1. 不应把所有的节点放在nodes中
      2. root, dir, file 应该使用不同的类, 而不是用变量进行区分
      3. 对于目录的扫描应该放到pyvim中. 目录与文件信息应该是可以共享的
"""

nodes = [  ]
win              = None
type_dir         = "dir"
type_root        = "root"
type_file        = "file"
index_separative = "<|>"

"""
    过滤相关函数
"""
blacklist_switch = True

blacklist_file=[ 
    "^\.",      "^tags$",
    ".+\.ac$", ".+\.pyc$" , ".+\.so$", ".+\.o$"
    ]

blacklist_dir=[ "^\..+", "PClint" ]

def black_filter_files( f ):
    if not blacklist_switch:
        return True
    for regex in blacklist_file:
        match = re.search( regex, f )
        if match:
            return False
    return True

def black_filter_dirs( f ):
    if not blacklist_switch:
        return True
    for regex in blacklist_dir:
        match = re.search( regex, f )
        if match:
            return False
    return True

"""
    排序函数
"""
def sorted_by_expand_name( files ):
    files_type = { "c":[], "cpp":[], "h":[], "py":[], "other":[] }
    types = files_type.keys( )

    for f in files:
        try:
            type_name = f.split( '.' )[ -1 ]
        except:
            type_name = "other"
        if not type_name in types:
            type_name = "other"
        files_type[ type_name ].append( f )
    tmp = [  ]
    for v in files_type.values( ):
        tmp += v

    return sorted(files_type[ 'c' ]) +\
            sorted(files_type[ 'cpp' ]) +\
            sorted(files_type[ 'h' ]) +\
            sorted(files_type[ 'py' ]) +\
            sorted(files_type[ 'other' ])



class  CNode( object ):
    """
        节点类
    """
    index = 0
    def __init__( self, name, deep, ctype, path , display = "" ):
        self.name = name
        self.deep = deep
        self.type = ctype
        self.path = path
        self.fold =True
        self.show = False  #判断目录是否打开
        self.fold_range = ( 0, 0 )
        self.index= self.index
        if not display:
            if self.type == type_dir:
                display  =  "%s +%s/" % ("  " * (self.deep  -1), name)
            elif self.type == type_file:
                if self.deep > 1:
                    display = "%s   %s" % ( " " * ((self.deep - 1) * 2 - 1), name )
                else:
                    display = "  %s" % name 
        if self.type == type_root:
                display = ">>>%s" % display
        self.display = "%s<|>%s" % ( display, self.index )
        self.__class__.index = self.index + 1

    def open_toggle( self, index_display ):
        if self.type in [ type_dir, type_root ]:
            self.__change_flag( index_display )
            if self.show:
                fun = pe_close_dir
            else:
                fun = pe_open_dir
            fun( self.index, index_display )
            return
        if self.type != type_file:
            return

        #上下文: 从path exp 窗口回到之前的窗口. 
        #行为:   不用执行autocmd
        #原因:   避免在path exp 窗口中显示当前窗口的位置. 因为当前的窗口就要关闭了
        vim.command( "noautocmd wincmd p" )

        if win == vim.current.window:
            return 
        vim.command( "update")
        vim.command( "e %s" % self.path )

    def keep_open( self, index_display ):
        if self.type in [ type_dir, type_root ]:
            if not self.show:
                self.__change_flag( index_display )
                pe_open_dir( self.index, index_display)

    def keep_close( self, index_display ):
        if self.type in [ type_dir, type_root ]:
            if self.show:
                self.__change_flag( index_display )
                pe_close_dir( self.index, index_display)

    def __change_flag( self, index_display ):
        line = vim.current.buffer[ index_display  ]
        if self.show:
            from_flag = "-"
            to_flag = "+"
        else:
            from_flag = "+"
            to_flag = "-"
        vim.current.buffer[ index_display ] = line.replace( from_flag, to_flag )

        
def pe_open_dir( index_node, index_display ):
    cur_node = nodes[ index_node ]
    cur_deep = cur_node.deep
    cur_node.show = True
    index_node += 1

    while index_node < len( nodes ):

        node = nodes[ index_node ]
        index_node += 1

        deep_space = node.deep - cur_deep
        if  deep_space == 1:
            vim.current.buffer.append( node.display, index_display + 1 )
            index_display += 1
            if node.type == type_dir and node.show :
                index_node, index_display = pe_open_dir( index_node,
                        index_display)
        elif deep_space <= 0:
            break
    return (index_node, index_display)

def pe_close_dir( index_node, index_display):
    cur_node = nodes[ index_node ]
    cur_deep = cur_node.deep

    cur_node.show = False
    if index_node + 1 == len( nodes ):
        return 
    for node in nodes[ index_node + 1: ]:
        deep_space = node.deep - cur_deep
        if deep_space == 1:
            index_node += 1
            if node.type == type_dir and node.show:
                pe_close_dir( index_node, index_display + 1 )
            del vim.current.buffer[ index_display + 1 ]

        elif deep_space <= 0:
            break




"""
    刷新
"""
def refresh_nodes(  ):
    del nodes[ : ]
    paths = mitems.settings.get( "paths" )
    if not paths:
        return None

    CNode.index = 0
    for info in paths:
        path = info.get( "path" )
        if not path:
            continue 
        if not os.path.exists( path ):
            pyvim.echoline('not dir:%s' % path)
            continue
        if path.endswith( '/' ):
            path = path[ 0:-1 ]

        display = info.get( "name" )
        name = os.path.basename( path )
        if not display:
            display  = name 

        nodes.append( CNode(name, 0, 'root', path, display ) )
        scan_dir( path, 1)



    

def scan_dir( dir_path, deep ):
    """
        扫描目录
    """
    d_f = os.listdir( dir_path )
    dirs = [  ]
    files = [  ]
    for f in d_f:
        path = os.path.join( dir_path, f )
        if os.path.isdir( path ):
            dirs.append( f )
        else:
            files.append( f )
    dirs = sorted( dirs )
    files = sorted_by_expand_name( files )


    for f in files:
        if black_filter_files( f ):
            nodes.append( CNode(f, deep , "file", os.path.join(dir_path, f)))

    for direct in dirs:
        if black_filter_dirs( direct ):
            t_path = os.path.join(dir_path, direct)
            nodes.append( CNode(direct, deep , "dir", t_path )) 
            scan_dir( t_path, deep + 1 )



class Routes( object ):
    """
        记录到某个node 的经历的root 与 dir, 最后一个也是目标
    """
    def __init__( self ):
        self.routes = None
        self.index = -1 
        self._found = False

    def init_route( self , path ):
        path = path.decode( 'utf8' )
        routes = [  ]
        for index, node in enumerate(nodes):
            if node.type == type_root:
                routes = [ index ] #routes 的第一个必然是root
                continue
            if len( routes ) <= node.deep:
                routes.append( index )
            else:
                routes[ node.deep ] = index
            if node.path == path:
                self._found = True
                routes = routes[ 0: node.deep + 1]
                break
        self.routes = routes
    def isfound(self):
        return self._found

    def hpop( self ):
        """
            从头开始提取route, 最后返回None
        """
        try:
            self.index += 1
            return self.routes[ self.index ]
        except:
            self.index = -1 
            return None
    def pop( self ):
        """
            pop 
        """
        return self.routes.pop( )



def goto_path_exp_win( ):
    if win and win.valid:
        try:
            vim.current.window = win

            return True
        except:
            pass
    return False

def open_to_file( path ):
    """
        file_path 必须是全路径
    """
    routes = Routes( )
    routes.init_route( path )
    if not routes.isfound():
        vim.current.window.cursor=(1, 0)
        return
    try:
        target = routes.pop( )
    except:
        return 
    buf = vim.current.buffer
    route = routes.hpop( )
    

    flag = 0
    for ii, line in enumerate(buf):
        try:
            index_node = int(line.split( index_separative )[ 1 ])
        except:
            continue

        if flag == 1:
            if index_node == target:
                line_nu = ii + 1
                vim.current.window.cursor=( line_nu , 0)
                #line_nu_top = int( vim.eval( "line('w0')" ) )
                #line_nu_bottom = int(  vim.eval( "line('w$')" ) )
                #if line_nu <  line_nu_top  or line_nu > line_nu_bottom:
                #vim.command( "redraw!" )

                break

        elif index_node ==  route:
            node = nodes[ index_node ]
            node.keep_open( ii )
            route = routes.hpop( )
            if route == None:
                flag = 1

        elif route == None :
            flag = 1



        


def refresh_win( ):
    global win
    if not win or win.valid == False:
        vim.command( "topleft 25vnew PathsExp" )
        vim.command( "set ft=paths_exp" )
        win = vim.current.window


    vim.current.window = win

    del vim.current.buffer[ : ]
    vim.current.buffer[ 0 ] = "PathsExp"


    for node in nodes:
        if node.deep == 0 :
            vim.current.buffer.append( node.display )
    return 

def paths_exp_open( ):
    """
        打开节点
    """
    index_display, c = vim.current.window.cursor
    line = vim.current.line.decode( 'utf8' )
    try:
        index_node = line.split( "<|>" )[ 1 ]
        index_node = int( index_node )
    except:
        return
    nodes[ index_node ].open_toggle( index_display - 1 )






"""
    API: 提供当前工程中的所的文件
"""
def get_files( ):

    all_files = [  ]
    root_len = 0
    for node in nodes:
        if node.deep == 0:
            root_len = len(node.path)
            if node.path[-1] != '/':
                root_len += 1
        if node.type != "file" or node.deep == 0:
            continue
        base = os.path.basename(node.path)
        dirname = os.path.dirname(node.path)[root_len:]
        if dirname:
            pre = "<span style='italic'>%s</span>/" % dirname
        else:
            pre = ""
        all_files.append( ( 
            pre, 
            base,
            node.path , 
            None) )
    return all_files




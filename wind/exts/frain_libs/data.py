#encoding:utf8
settings = { "paths":[  ] }
"""such as: {
      "paths":
      [
            {
                "path":"/path/to",
                "name":"name"
            },
            {
                "path":"/path/to",
                "name":"name"
            }
       ]
"""


all_items_info = [  ]
mode = False


"""
    管理工程相关的数据.
"""

#作用:  为setting 增加一个path
class PathInfo:
    def __init__( self ):
        self.name = ""
        self.path = ""

def append_path( path, name="" ):
    paths = settings.get( "paths" )
    path_info =  {"path": path, "name": name}
    if paths:
        settings[ "paths" ].append( path_info )
    else:
        settings[ "paths" ] = [ path_info ]


#得到当前所有的工程的根目录列表
def get_path( ):
    paths_out = [  ]
    paths = settings.get( "paths" )
    if not paths:
        return paths_out
    for info in paths:
        path = info.get( "path" )
        paths_out.append( path )
    return paths_out


#得到当前settings 中的目录
def get_pathinfo( ):
    paths = settings.get( "paths" )
    if not paths:
        return [  ]
    for info in paths:
        path = info.get( "path" )
        if not path:
            continue 
        if not os.path.exists( path ):
            continue
        if path.endswith( '/' ):
            path = path[ 0:-1 ]
        return 

        display = info.get( "name" )
        name = os.path.basename( path )
        if not display:
            display  = name 

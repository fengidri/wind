#encoding:utf8
import pyvim
import vim

from frain_libs import mitems 
from frain_libs import paths_exp
from frain_libs import data


from frain_libs import project 

from vuirpc import VuiClient

from frain_libs import fropen
from frain_libs import frnames
from frain_libs import mescin



class FrainOpenDir( pyvim.command ):
    def run( self ):
        if not self.params:
            return
        mitems.frain_open_dir( self.params[0] )
        data.mode = True

    def setting( self ):
        self.set_complete( self.complete_file )

#class FrainClose( pyvim.events ):
#    def on_VimLeavePre( self ):
#        if not data.mode:
#            return
#        mitems.close( )
#



#############################
# path exp
#############################
class PathsExp( pyvim.command ):
    def run( self ):
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )

class PathsExpFilter( pyvim.command ):
    def run( self ):
        paths_exp.blacklist_switch = not paths_exp.blacklist_switch
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )

class PathsExpRefresh( pyvim.command ):
    def run( self ):
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )
        #刷新path exp 窗口之后. 展开显示当前正在编辑的文件
        for w in vim.windows:
            b = w.buffer
            if b.options['buftype'] != '':
                continue
            paths_exp.open_to_file( b.name )

class PathsExpOpen( pyvim.command ):
    def run( self ):
        paths_exp.paths_exp_open( )

class PathsExpSwitch( pyvim.command ):
    def run( self ):
        paths_exp.switch_file_quick( )

class PathsExpFind( pyvim.command ):
    def run( self ):
        path = pyvim.vim.current.buffer.name
        if not path:
            return
        if pyvim.vim.current.buffer.options['buftype'] != '':
            return 
        if paths_exp.goto_path_exp_win( ):
            paths_exp.open_to_file( path )

class PathsExpGo(pyvim.command):
    def run(self):
        paths_exp.goto_path_exp_win( )



class Project( pyvim.command ):
    def run( self ):
        def popen(response):
            fropen(response.msg)
        client = VuiClient()
        client.sethandle(200, popen)
        client.request("/open/project", {"values":frnames()})
        client.response()

class ProjectNew( pyvim.command ):
    def run( self ):
        mescin.create_cfg()


class ProjectSync( pyvim.command ):
    def run( self ):
        if not project.Project:
            return
        project.Project.sync( )
"""
    -- 无视时间, 同步所有的文件
"""
class ProjectSyncAll( pyvim.command ):
    def run( self ):
        if not project.Project:
            return
        project.Project.sync( syncall=True )




class ProjectEvent( pyvim.events ):
    def on_VimLeave( self ):
        if not project.Project:
            return
        project.Project.on_close( )













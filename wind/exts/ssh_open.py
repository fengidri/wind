import pyvim
import vim

import ssh2
import sshm
import os
#import wx_notify

class ssh_edit( object ):
    def __init__( self ):
        self.remote_info = None
        self.remote_path = None
        self.local_path =None
    def connect( self ):
        ssh = ssh2.ssh2( )
        ssh.connect( self.remote_info.ip,
                self.remote_info.root,
                self.remote_info.password,
                self.remote_info.port
                )
        return ssh.open_session( )
    def edit( self, path_to_file):
        """
            path_to_file:
                192.168.1.1:/etc/ssh/sshd_config
        """
        ip, path = path_to_file.split( ":" )
        self.remote_path = path
        base_name = os.path.basename( path )
        dir_name = os.path.dirname( path )

        dir_local = "/tmp/@%s%s" %( ip, dir_name)

        self.remote_info = sshm._sshrc( ).get_item_by_host( ip )
        local_path = os.path.join(dir_local, base_name) 
        self.local_path = local_path

        try:
            os.makedirs( dir_local )
        except OSError:
            pass

        session = self.connect( )
        session.scp_recv( path, local_path)
        vim.command( "edit %s"% local_path )
    def send( self ):
        session = self.connect( )
        session.scp_send( self.local_path, self.remote_path )






SSH_EDIT_LIST = {  }




class SSHedit( pyvim.command ):
    def run( self ):
        edit = ssh_edit( )
        SSH_EDIT_LIST[ vim.current.buffer ] = edit
        if not self.params:
            return
        edit.edit( self.params[0] )
        vim.command( "auto BufWritePost <buffer> SSHsend")

class SSHsend( pyvim.command ):
    def run( self ):
        vim.command( "update" )
        edit = SSH_EDIT_LIST.get( vim.current.buffer )
        if  edit == None:
            return
        edit.send( )


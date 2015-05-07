#encoding:utf8
import time
import os
import stat
import tarfile
import StringIO
import ssh2
import yaml
import sys
import re


class Conf( object ):
    def __init__( self ):
        pass

    def read_conf( self, config_file ):
        self.config_file = config_file
        if os.path.isfile( self.config_file ):
            self.cf = yaml.load(open( self.config_file ))
        else:
            self.cf = self.create_cfg( )

        self.c_host= self.cf[ 'compile' ][ 'host' ]
        self.c_ssh_port=self.cf[ 'compile' ][ 'ssh_port' ]
        self.c_ssh_user=self.cf[ 'compile' ][ 'ssh_user' ]
        self.c_password=self.cf[ 'compile' ][ 'ssh_password' ]


    def section( self, name):
        for item in self.cf:
            if name in item.keys( ):
                return item.get( name )




    def timestamp( self, timestamp=None ):
        item = self.cf.get( 'projects' )
        for p in item:
            if p[ 'path' ] == self.l_root_dir:
                break
        if timestamp:
            p[ 'timestamp' ] = timestamp
        return p[ 'timestamp' ]


        cf.write( open(self.config_file, 'w') )







class Src_files( object ):
    """
        查找path 下的时间在timestamp 之后的文件
    """
    file_black_list = [ "^\.", "\.ncb$",  '\.sln$', '\.suo$', '\.vcproj$', '\.o$',
            "^lib\w+\.so\.", "\.lib$", "Makefile.in", "tags" ]
    dir_black_list= [ "\.svn" ]

    def __init__( self, timestamp, path ):
        if isinstance( timestamp, str ):
            self.timestamp = int(timestamp.split('.')[0])
        else:
            self.timestamp = timestamp

        self.path = path
        if path.endswith( '/' ):
            self.length = len( path )
        else:
            self.length = len( path ) + 1


    def filter( self, name , root):
        """
            过滤文件.
        """
        for regex in self.file_black_list:
              if re.search( regex, name ):
                 return False
        if self.timestamp > 0:
            if os.stat( os.path.join(root, name))[ stat.ST_MTIME ]\
                 < self.timestamp:
                     return False
        return True
    def scan( self ):
        src_files=[  ]
        for root, subdirs, files in os.walk( self.path ):
            for regex in self.dir_black_list:
                if re.search( regex, root ):
                     continue
            for f in files:
                if not self.filter( f, root ):
                    continue
                src_files.append( os.path.join(
                    root[ self.length:], f)
                    )
        return src_files

class SSH_Options( object ):
    """
        SSH 低层操作
    """
    def __init__( self, host, user, pwd, port ):
        cir_ssh = ssh2.ssh2()
        cir_ssh.connect(  host, user, pwd, port)
        self.session =  cir_ssh.open_session( )

    def mem_to_remote( self,  mem, path ):
        """
            作用: 把mem 中的tar 数据在path 下进行解压
        """
        cmd = "mkdir -p {path};> /tmp/pack;tar xmf /tmp/pack -C {path}".format( path = path )

        chan = self.session.open_chan( )
        chan.execute( cmd, out_merge = True)
        "发送数据"
        stdin = chan.stdin( )


        #此处 ssh4py 有bug. 如果数据大于缓冲区时, 不会续传余下的
        left = len( mem )
        length = left
        while( left > 0 ):
            n_send = stdin.write( mem[ length - left :]   )
            left = left -  n_send
        stdin.close( )


class SSH_SCIR( object ):
    """
        基于低层SSH API 为上层提供接口
    """
    def __init__( self,  host, user, pwd, port ):
        self.c_ssh = SSH_Options( host, user, pwd, port )

    def scp_to_compile( self, context, c_path ):
        self.c_ssh.mem_to_remote( context, c_path )





class SCIR( object ):
    def __init__( self):

        #用于标准输出
        self.stdout = sys.stdout
        

        self.loging= sys.stdout
    def c_connect( self,  host, user, pwd, port=22 ):
        self.c_client = SSH_SCIR( host, user, pwd, port )


    
    def sync( self, timestamp, path, c_path ):

        "过滤出要同步的文件"
        src_files= Src_files( timestamp, path).scan( )
        if len( src_files )==0:
            self.stdout.write(  "<<<No files to sync.>>>\n"  )
            return -1

        "输出到 统一 输出 会同步的文件"
        out_msg = "Sync [%s]=>[%s]:[%s]\n" % ( path,
                c_path, len(src_files))

        self.stdout.write( out_msg )


        "切换到工作目录"
        os.chdir( path )

        "生成 tar bz2 文件"
        mem_tar = StringIO.StringIO( )
        tar = tarfile.open( fileobj=mem_tar, mode='w:bz2' )
        for f in src_files:
            tar.add( f )
        tar.close( )
        self.stdout.write( "Send...\n" )
        
        mem_tar.seek( 0 )


        self.c_client.scp_to_compile( mem_tar.read(), c_path )
        mem_tar.close( )

        self.stdout.write( "<<<Sync over.>>>\n" )

    def _save_timestamp( self ):

        "保存同步时间"
        self.conf.timestamp( time.time() )
        self.conf.close( )




if __name__ == "__main__":
    obj = SCIR( )
    obj.c_connect( "192.168.72.205", "feng", "idri")
    obj.sync( 0, "/home/VOS/VOS/vos_1.0/callserver/", "/tmp/b2bua" )

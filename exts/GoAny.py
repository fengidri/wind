#encoding:utf8
import pyvim
import os
import vim
from vuirpc import VuiClient

class GoAny( pyvim.command ):
    def run( self ):
        vim.command("update")
        vim.command("normal m'")
        gototag()
        return

#class GoFile(pyvim.command):
#    def run(self):
#        gotofile()
#


def get_file_tag( file_name ):
    flag = {"f":"<span color='blue'>ℵ</span> ",
            "m":"<span color='green'>✢</span> ",
            'v':"<span color='red'>⋎</span> "}
    all_var = [  ]
    if not file_name:
        return all_var
    cmd = "ctags --sort=no -f - -n --fields=-lzf %s" % file_name
    f = os.popen( cmd )

    for line in f.readlines( ):
        tmp = line.split( )
        keyword= tmp[0] #tag name
        keyword_type = tmp[ 3 ] # 类型如 f
        linenu = tmp[ 2 ][ 0: -2 ]# 行号, ctag 输出如: 114;"

        if not keyword_type in "fmv":# 只取变量
            continue

        if len(tmp) > 4:# 最一列用于记录所属的类或结构体
            keyword = "%s:%s" % (tmp[ 4 ]  , keyword)

        pre = flag.get(keyword_type, " ")
        all_var.append( (
            pre,  # for display
            keyword ,# for filter
            linenu , # the value
            None
            ) )
    return all_var
####################################################################
#callback
def showpos(response):
    try:
        linenu = int(response.msg)
    except:
        return
    vim.current.window.cursor = ( linenu, 0 )
    vim.command("normal zt")
    pyvim.redraw()
    pyvim.echoline(response.msg)

def showfile(response):
    filepath = response.msg
    vim.command("silent edit %s" % filepath)
    pyvim.redraw()
    pyvim.echoline(filepath)

####################################################################

def gototag():
    backpos = vim.current.window.cursor

    client = VuiClient()
    client.sethandle(110, showpos)
    client.sethandle(200, showpos)
    client.request("/open/tag", {"values":
        get_file_tag(vim.current.buffer.name)})
    response = client.response()
    if response.code > 200:
        vim.current.window.cursor = backpos
        pyvim.echoline("Quit")


#def gotofile():
#    curfile = vim.current.buffer.name
#    msg = {"values": frfiles()}
#
#    client = VuiClient()
#    client.sethandle(110, showfile)
#    client.sethandle(200, showfile)
#    client.request("/open/file", msg)
#
#    response = client.response()
#    if response.code > 200:
#        vim.command("silent edit %s" % curfile)
#        pyvim.echoline("Quit")
#
#


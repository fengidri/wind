#encoding:utf8
import pyvim
import vim
import os
import re

@pyvim.cmd()
def FSearch(sel = False):
    if not sel:
        word = "\<%s\>" % pyvim.current_word()
    else:
        word = pyvim.select()
        word = word.replace("'", "\\'")
    pyvim.log.info(">%s", word)

    filter = ''

    command, path = context(word, filter)

    if not command:
        return

    f_popen = os.popen(command)
    lines = f_popen.readlines()
    if lines:
        filter_quick( lines, path, command )


"""
    处理编码问题
"""
def byte_to_unicode( byte ):
    try:
        "UTF8"
        byte = byte.decode( "utf8" )
    except UnicodeDecodeError:
        "GBK"
        byte = byte.decode( "GB18030" )
    except UnicodeDecodeError:
        byte = None
    return byte


"""
    分析上下文
"""
def context(word, filter=""):
    target = ""
    dirname = ""
    suffix = ['*.[ch]', '*.cpp', '*.cc', '*.py']

    cur_path = vim.current.buffer.name
    if not cur_path:
        return None, None

    for path in pyvim.Roots:
        if cur_path.startswith( path ):
            include = [" --include='%s' " % s for s in suffix ]
            include = ' '.join(include)

            dirname = path
            break
    else:
        include = ""
        target =  os.path.basename( cur_path )
        dirname = os.path.dirname( cur_path )


    if  dirname in [ "/", "/home", os.environ.get("HOME") ]:
        return None,None

    cmd = "cd {dirname};grep -RHn --binary-file=without-match "\
            "{include} '{word}' {target} "

    cmd.format( dirname = dirname, include = include, word    = word,
            target  = target,)

    return cmd, dirname

"""
    对于结果进行过滤, 打开quickfix
"""
def filter_quick( lines, path, command ):
    tmp_file = '/tmp/vimgrep'
    grep_output = u"Grep Entering directory '%s'\n%s\n\n"  % (path, command)
    outs=[ grep_output ]
    for l in  lines:
        line = byte_to_unicode( l )
        if not line:
            vim.command( "echom  'I do not know this code [%s]'" % l)
            return

        if re.search(r"^[^ ]+\| \s*//", line):
            continue
        line = line.replace('\r','')
        outs.append( line )

    #写入文件之前转换成字节码
    context = u''.join(outs).encode('utf8' )
    f = open(tmp_file, 'w')
    f.write(context )
    f.close()

    pyvim.quickfix_read_error( tmp_file )
    lines_nu = len(outs) + 3
    if lines_nu > 15:
        lines_nu = 15
    pyvim.quickfix( lines_nu )

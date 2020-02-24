#encoding:utf8
import pyvim
import vim
import os
import re

SUFFIX = ['*.[ch]', '*.cpp', '*.cc', '*.py']

def search(word, target = ''):
    command, path = context(word, target = target)

    if not command:
        return

    pyvim.log.error("search cmd: %s", command)
    f_popen = os.popen(command)
    lines = f_popen.readlines()
    if lines:
        filter_quick( lines, path, command )


@pyvim.cmd()
def FSearch(word):
    f = vim.current.buffer.name
    if f:
        f = os.path.basename(f)
        f = f.split('.')
        if len(f) > 1:
            suffix = '*.%s' % f[-1]
            if suffix not in SUFFIX:
                SUFFIX.append(suffix)


    search(word)


@pyvim.cmd()
def FSearchX(sel = False):
    if not sel:
        word = "\<%s\>" % pyvim.current_word()
    else:
        word = pyvim.select()
        word = word.replace("'", "\\'")
    pyvim.log.error(": %s", word)

    search(word)


@pyvim.cmd()
def FSearchLinux(_sub = ''):
    root = pyvim.get_cur_root()
    if not root:
        return

    f = vim.current.buffer.name.split('/')
    t = root.split('/')
    if t[-1] == '':
        sub = f[len(t) - 1]
    else:
        sub = f[len(t)]


    target = 'include %s %s' % (sub, _sub)
    word = "\<%s\>" % pyvim.current_word()

    search(word, target)





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
def context(word, target = ''):
    dirname = ""

    cur_path = vim.current.buffer.name
    if not cur_path:
        return None, None

    root = pyvim.get_cur_root()
    if root:
        include = [" --include='%s' " % s for s in SUFFIX ]
        include = ' '.join(include)

        dirname = root
    else:
        include = ""
        target =  os.path.basename( cur_path )
        dirname = os.path.dirname( cur_path )


    if  dirname in [ "/", "/home", os.environ.get("HOME") ]:
        return None,None


    cmd = "cd {dirname};grep -RHn --binary-file=without-match "\
            "{include} '{word}' {target} "

    cmd = cmd.format( dirname = dirname, include = include, word    = word,
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
        line = l
        #line = byte_to_unicode( l )
        if not line:
            vim.command( "echom  'I do not know this code [%s]'" % l)
            return

        if re.search(r"^[^ ]+\| \s*//", line):
            continue
        line = line.replace('\r','')
        outs.append( line )

    #写入文件之前转换成字节码
    context = u''.join(outs)
    f = open(tmp_file, 'w')
    f.write(context )
    f.close()

    pyvim.quickfix_read_error( tmp_file )
    lines_nu = len(outs) + 3
    if lines_nu > 15:
        lines_nu = 15
    pyvim.quickfix( lines_nu )

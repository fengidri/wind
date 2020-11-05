#encoding:utf8
import pyvim
import vim
import os
import re

SUFFIX = ['*.[ch]', '*.cpp', '*.cc', '*.py', '*.S']
EX_SUFFIX= ['*.mod.c']

def search(word, target = ''):
    command, path = context(word, target = target)

    if not command:
        return

    pyvim.log.error("search cmd: %s", command)
    f_popen = os.popen(command)
    lines = f_popen.readlines()
    if lines:
        filter_quick(word, lines, path, command )


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

        exclude = [" --exclude='%s' " % s for s in EX_SUFFIX ]
        exclude = ' '.join(exclude)

        dirname = root
    else:
        include = ""
        exclude = ""
        target =  os.path.basename( cur_path )
        dirname = os.path.dirname( cur_path )


    if  dirname in [ "/", "/home", os.environ.get("HOME") ]:
        return None,None


    cmd = "cd {dirname};grep -RHn --binary-file=without-match "\
            "{include} {exclude} '{word}' {target} "

    cmd = cmd.format(dirname = dirname,
            word    = word,
            include = include,
            exclude = exclude,
            target  = target,)

    return cmd, dirname

"""
    对于结果进行过滤, 打开quickfix
"""
def filter_quick(word, lines, root, command = '' ):
    tmp_file = '/tmp/vimgrep'
    outs = []
    outs.append(">> %s\n" % word)
    outs.append(u"Entering directory '%s'\n"  % root)
    outs.append(u"%s\n" % command)
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

    # 下面会打开 quickfix window,
    # 在进入 window 之后 path 应该是由于 autochdir
    # 会发现变化, 所以这里把 autochdir 先关闭掉.
    # 并设置 path 到 root, 这样 quickfix 在
    # 显示 filepath 的时候才会基于 root 进行显示,
    # 不然会基于当前目录进行显示, 导致其它
    # 目录下的文件名特别长
    vim.command('set noautochdir')
    os.chdir(root)

    pyvim.quickfix_read_error( tmp_file )
    lines_nu = len(outs) + 3
    if lines_nu > 15:
        lines_nu = 15
    pyvim.quickfix( lines_nu )

    vim.command('set autochdir')



@pyvim.cmd()
def Quickfix(path):
    lines = open(path).readlines()
    root = pyvim.get_cur_root()
    filter_quick('', lines, root)

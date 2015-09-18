#encoding:utf8
import vim
import os
import pyvim
import ctags
import sys
import logging

# new tags

def encode(cmd):
    # 把 tags 文件的里 命令式 tag 进行转码
    show_enco=vim.eval('&encoding')
    file_enco=vim.eval('&fileencoding')
    if file_enco != show_enco:
        if file_enco:
            cmd = cmd.decode(file_enco).encode(show_enco)
    return cmd




class TagList:
    tagsfile = ''
    list_tags = []
    def __init__( self, root_dir ):
        self.tagfile = None
        self.tag_root_dir = root_dir
        self.tags = "%s/tags" % root_dir
        self.open(  )
    def open(self):
        self.items = None
        self.funs= None
        tagsfile = self.tags
        if os.path.isfile(tagsfile):
            self.tagsfile = tagsfile;
            self.tagfile = ctags.CTags(self.tagsfile)
            self.entry = ctags.TagEntry()
            return True
        else:
            logging.error( '%s is no tags.' % tagsfile)
            return False
    def get_items( self ):
        if self.items == None:

            items = [  ]
            status = self.tagfile.find(self.entry, '', ctags.TAG_PARTIALMATCH )
            while ( status ):
                items.append( self.entry["name"] )
                status = self.tagfile.findNext(self.entry)
            self.items = items
        return self.items
    def get_funs( self ):
        if self.funs == None:

            funs = [  ]
            status = self.tagfile.find(self.entry, '', ctags.TAG_PARTIALMATCH )
            while ( status ):
                if self.entry[ "kind" ] == 'f':
                    funs.append( self.entry["name"] )
                status = self.tagfile.findNext(self.entry)
            self.funs = funs
        return list(set(self.funs ))

    def out_list(self, tag, MODE=ctags.TAG_FULLMATCH):
        "输出关于tag的所有信息"
        if not self.tagfile:
            self.open( )
            if self.tagfile == None:
                vim.command( "echo 'no tagfile'")
                return None

        list_tags = []
        status = self.tagfile.find(self.entry, tag, MODE )
        if not status:
            return None
        while ( status ):
            list_tags.append(self.entry_to_dict(self.entry))
            status = self.tagfile.findNext(self.entry)
        return list_tags
    def entry_to_dict(self, entry):
        edict = { }
        edict["tag"] = entry["name"]
        edict["filename"] = os.path.join( self.tag_root_dir, entry["file"] )
        edict["cmd"] = entry["pattern"]
        edict["lineNumber"]  = entry["lineNumber"]
        edict["kind"] = entry["kind"]
        return edict

    def refresh( self ):
        if self.tag_root_dir:
            os.popen("cd %s;ctags -R *"  % self.tag_root_dir )
            vim.command("echo 'the ctags is ok'")
            self.open( )
        else:
            logging.error("this is not a project" )



class class_tag:
    wstacks = { }
    last_tag = ''
    def __init__(self):
        self.inited = 1
        self.tagsfile_list = [  ]
        for path in pyvim.Roots:
            self.tagsfile_list.append( TagList(path) )

    def refresh( self ):
        for tagfile in self.tagsfile_list:
            tagfile.refresh( )

    def jump(self, tag):
        "跳转入口"
        if tag == self.lasttag():
            #相同的tag  平行跳转
            self.open_tag()
        else:
            #新的tag     纵向跳转
            if not self.add_tag(tag):
                return  -1
            self.open_tag()

        try:
            vim.command('normal zz')
            #vim.command('%foldopen!')
        except vim.error, e:
            logging.error(e)


    def add_tag(self, tag):
        if not self.tagsfile_list:
            logging.error( 'this is not a project context')
            return 0

        for tagsfile in self.tagsfile_list:
            taglist = tagsfile.out_list(tag)
            if taglist:
                break

        if not taglist:
            return 0

        num = len(taglist)
        start_file = pyvim.filepath( )
        start_file_pos = vim.current.window.cursor

        "加入到stack中tag从定义处开始"
        for pos, taginfos in enumerate(taglist):
            if taginfos['kind']  == 'function':
                break
            if taginfos['kind']  == 'variable':
                break

        #加入到stack中去
        self.append(taglist,
                tag,
                num,
                pos,
                start_file,
                start_file_pos)
        return True

    def back(self):
        taginfo  = self.taginfo()
        self.pop()
        if not taginfo:
            vim.command(" echo 'there is no tag in stack'")
            return 0

        pre_buffer_name=vim.current.buffer.name

        vim.command('update')
        vim.command('silent edit %s'  %  taginfo["start_file"])

        line_nu= taginfo["start_file_pos"][0]
        col_nu= taginfo["start_file_pos"][1]
        vim.current.window.cursor = (line_nu, 0)
        vim.command("normal %sl"  % col_nu)




        try:
            vim.command('%foldopen!')
        except vim.error, e:
            pass

        try:
            vim.command('normal zz')
        except vim.error, e:
            logging.error(e)


    def open_tag(self):
        taginfo         = self.taginfo()
        taglist         = taginfo["taglist"]
        tagname         = taginfo["tagname"]
        num_total       = taginfo["num_total"]
        pos_for_taglist = taginfo["pos_for_taglist"]

        if taginfo["num_total"]  == 0:
            vim.command("echo 'not find'")
            return 0

        #echo
        vim.command("echo '%s %s %s/%s'"  % (
            taginfo['tagname'],
            taglist[pos_for_taglist]['kind'],
            pos_for_taglist  + 1,
            num_total))

        taginfo_path = taglist[pos_for_taglist]['filename']
        if taginfo_path != vim.current.buffer.name:
                #保存文件
                vim.command('silent update')
                vim.command("silent edit %s"  %  taginfo_path)
        #cmd  #go to the tag
        try:
            cmd = taglist[pos_for_taglist]['cmd']

            cmd = encode(cmd)
            #定位光标到tag上
            line_nu = 0
            found = [  ]
            if cmd.isdigit():
                line_nu = int(cmd)   - 1
                found.append( line_nu )
            else:
                patten = cmd[2: -2].replace(r'\/','/')
                patten = patten.replace(r'\r','')
                for line in vim.current.buffer:
                    if line.startswith(patten):
                        found.append( line_nu  )
                    line_nu+=1

            if found:
                line_nu = found.pop( )
                line = vim.current.buffer[line_nu]
                col_nu = line.find(tagname)
                if col_nu < 0:
                    col_nu = 0

                vim.current.window.cursor = (line_nu  + 1, 0)
                vim.command("normal %sl"  % col_nu)
            else:
                logging.info('patten'+patten)

        except vim.error, e:
            logging.error(e)
            return  -1


        pos_for_taglist+= 1
        if pos_for_taglist>= num_total:
            pos_for_taglist  = 0
        taginfo["pos_for_taglist"]  = pos_for_taglist

        #pyvim.highlight()


@pyvim.cmd()
def CTagJump(tag = None):
    global Tag
    if Tag == None:
        Tag = class_tag()

    if not tag:
        tag = pyvim.current_word()

    Tag.jump(tag)

@pyvim.cmd()
def CTagBack():
    wstack = pyvim.WStack()
    pos = wstack.pop()
    if not pos:
        pyvim.echo('there is no tag in stack')
        return 0

    cur_bn = vim.current.buffer.number
    wst_bn = wstack[0]

    if wst_bn != cur_bn:
        vim.command('update')

    vim.command("buffer %s" % wst_bn)

    vim.current.window.cursor = wstack[1]

    try:
        vim.command('%foldopen!')
    except vim.error, e:
        pass

    try:
        vim.command('normal zz')
    except vim.error, e:
        logging.error(e)


@pyvim.cmd()
def CTagRefresh():
    global Tag
    if Tag == None:
        return
    Tag.refresh( )


if not __name__== "__main__":
    Tag = None


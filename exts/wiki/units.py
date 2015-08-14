# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-14 13:50:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import tempfile

SERVER      = vim.vars.get("wind_wiki_server")
URL_INDEX   = vim.vars.get("wind_wiki_index")
URL_CHAPTER = vim.vars.get('wind_wiki_chapter')      # 后缀用于临时文件的类型
URL_PUT     = vim.vars.get("wind_wiki_api_chapter")
URL_POST    = vim.vars.get("wind_wiki_api_chapters")

def tmpfile():
    sf = ".%s" % URL_CHAPTER.split('.')[-1]
    return tempfile.mktemp(suffix=sf, prefix='fwiki_')

if __name__ == "__main__":
    pass


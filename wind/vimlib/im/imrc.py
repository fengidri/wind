# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-10 18:15:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import os
import string

wbcpickle = os.path.join(os.path.dirname(__file__), 'wbtree.cpickle').replace('\\','/')
wbtxt = os.path.join(os.path.dirname(__file__), 'wubi.txt').replace('\\','/')
fa_rule = """

>*
    *            base
    String       wubi

>c,cpp,python,javascript,ch,vim
    *            code
    CCommentDesc wubi
    CCommentArg  wubi
    Constant     wubi
    Comment      wubi
    String       wubi

>html
    *            wubi
    String       wubi
    cssStyle     code
    Statement    code
    Function     html
    Type         code
>context
    *            wubi
    Identifier   code
    Statement    code
>svn,gitcommit,markdown
    *            wubi

"""

digits = [ d for d in string.digits ]
lowerletter = [ c for c in string.ascii_lowercase ]
upperletter = [ c for c in string.ascii_uppercase ]
# TODO 要对于key 更加详细的划分
puncs = {
             # "vim name"  "see"      "feed"
      "parenthess"         : ["("       ,  "("          ] ,
      "bracket"            : ["["       ,  "["          ] ,
      "brace"              : ["{"       ,  "{"          ] ,
      "mark"               : ["'"       ,  "'"          ] ,
      "comma"              : [","       ,  ","          ] ,
      "semicolon"          : [";"       ,  ";"          ] ,
      "minus"              : ["-"       ,  "-"          ] ,
      "underline"          : ["_"       ,  "_"          ] ,
      "add"                : ["+"       ,  "+"          ] ,
      "precent"            : ["%"       ,  "%"          ] ,
      "and_"               : ["&"       ,  "&"          ] ,
      "lt"                 : ["<"       ,  "<"          ] ,
      "gt"                 : [">"       ,  ">"          ] ,
      "cat"                : ["^"       ,  "^"          ] ,
      "not_"               : ["!"       ,  "!"          ] ,
      "dot"                : ["."       ,  "."          ] ,
      "slash"              : ["/"       ,  "/"          ] ,
      "eq"                 : ["="       ,  "="          ] ,
      "double_mark"        : ['"'       ,  '"'          ] ,
      "tab"                : ['<tab>'   ,  '\<tab>'     ] ,
      "backspace"          : ['<bs>'    ,  '\<bs>'      ] ,
      "enter"              : ['<cr>'    ,  '\<cr>'      ] ,
      "space"              : ['<space>' ,  '\<space>'   ] ,
      "esc"                : ['<esc>'   ,  '\<esc>'     ] ,
        }

mults = {
            "jump"  :  ['<c-j>',        '\<c-j>'     ],
        }



count = 0  # 
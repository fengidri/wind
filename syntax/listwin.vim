"author:丁雪峰feng idri
"time:2013-11-22
"这个文件是对于nerdtree 的彩色的补充"
"
"下面是对于c语言的工程中的头文件与定义文件的文件名彩色化
"
"针对于c  cpp 定义文件，使用相同的色彩，因为同个工程中一般不会同时使用cpp与c
"并且其在工程中的作用是相同的
syn match PATHS_TITLE           #^>>>[a-zA-Z0-9_ -.]\+#

syn match PATHS_EXPFileTypePy   #.\+\.py\>#
syn match PATHS_EXPFileTypeLua  #.\+\.lua\>#
syn match PATHS_EXPFileTypeSh   #.\+\.mk\>#
syn match PATHS_EXPFileTypeSh   #.\+\.sh\>#
syn match PATHS_EXPFileTypeC    #.\+\.c\>#
syn match PATHS_EXPFileTypeC    #.\+\.cpp\>#
syn match PATHS_EXPFileTypeC    #.\+\.cc\>#
syn match PATHS_EXPFileTypeH    #.\+\.h\>#
syn match PATHS_EXPFileTypeJS   #.\+\.js\>#
syn match PATHS_EXPFileTypeHtml #.\+\.html\>#
syn match PATHS_EXPFileTypeHtml #.\+\.tpl\>#
syn match PATHS_EXPTreeDirName  #[+-].\+/#
"以.h结尾的文件使用另一种色彩"

hi clear Folded
"hi clear Cursor


let s:tree_up_dir_line = '.. (up a dir)'
"PATHS_EXPTreeFlags are syntax items that should be invisible, but give clues as to
"how things should be highlighted
syn match PATHS_EXPTreeFlag #\~#
syn match PATHS_EXPTreeFlag #\[RO\]#

"highlighting for the .. (up dir) line at the top of the tree
execute "syn match PATHS_EXPTreeUp #\\V". s:tree_up_dir_line ."#"

"highlighting for the ~/+ symbols for the directory nodes
syn match PATHS_EXPTreeClosable #\~\<#
syn match PATHS_EXPTreeClosable #\~\.#
syn match PATHS_EXPTreeOpenable #+\<#
syn match PATHS_EXPTreeOpenable #+\.#he=e-1

"highlighting for the tree structural parts
syn match PATHS_EXPTreePart #|#
syn match PATHS_EXPTreePart #`#
syn match PATHS_EXPTreePartFile #[|`]-#hs=s+1 contains=PATHS_EXPTreePart

"quickhelp syntax elements
syn match PATHS_EXPTreeHelpKey #" \{1,2\}[^ ]*:#hs=s+2,he=e-1
syn match PATHS_EXPTreeHelpKey #" \{1,2\}[^ ]*,#hs=s+2,he=e-1
syn match PATHS_EXPTreeHelpTitle #" .*\~#hs=s+2,he=e-1 contains=PATHS_EXPTreeFlag
syn match PATHS_EXPTreeToggleOn #".*(on)#hs=e-2,he=e-1 contains=PATHS_EXPTreeHelpKey
syn match PATHS_EXPTreeToggleOff #".*(off)#hs=e-3,he=e-1 contains=PATHS_EXPTreeHelpKey
syn match PATHS_EXPTreeHelpCommand #" :.\{-}\>#hs=s+3
syn match PATHS_EXPTreeHelp  #^".*# contains=PATHS_EXPTreeHelpKey,PATHS_EXPTreeHelpTitle,PATHS_EXPTreeFlag,PATHS_EXPTreeToggleOff,PATHS_EXPTreeToggleOn,PATHS_EXPTreeHelpCommand

"highlighting for readonly files
syn match PATHS_EXPTreeRO #.*\[RO\]#hs=s+2 contains=PATHS_EXPTreeFlag,PATHS_EXPTreeBookmark,PATHS_EXPTreePart,PATHS_EXPTreePartFile

"highlighting for sym links
syn match PATHS_EXPTreeLink #[^-| `].* -> # contains=PATHS_EXPTreeBookmark,PATHS_EXPTreeOpenable,PATHS_EXPTreeClosable,PATHS_EXPTreeDirSlash

"highlighing for directory nodes and file nodes
syn match PATHS_EXPTreeDirSlash #/#
syn match PATHS_EXPTreeDir #[+-].*/# contains=PATHS_EXPTreeLink,PATHS_EXPTreeDirSlash,PATHS_EXPTreeOpenable,PATHS_EXPTreeClosable,FrainUIRed,FrainUIBlue,FrainUIGreen
syn match PATHS_EXPTreeExecFile  #[|` ].*\*\($\| \)# contains=PATHS_EXPTreeLink,PATHS_EXPTreePart,PATHS_EXPTreeRO,PATHS_EXPTreePartFile,PATHS_EXPTreeBookmark
syn match PATHS_EXPTreeFile  #|-.*# contains=PATHS_EXPTreeLink,PATHS_EXPTreePart,PATHS_EXPTreeRO,PATHS_EXPTreePartFile,PATHS_EXPTreeBookmark,PATHS_EXPTreeExecFile
syn match PATHS_EXPTreeFile  #`-.*# contains=PATHS_EXPTreeLink,PATHS_EXPTreePart,PATHS_EXPTreeRO,PATHS_EXPTreePartFile,PATHS_EXPTreeBookmark,PATHS_EXPTreeExecFile
syn match PATHS_EXPTreeCWD #^[</].*$#

"highlighting for bookmarks
syn match PATHS_EXPTreeBookmark # {.*}#hs=s+1

"highlighting for the bookmarks table

hi def link PATHS_EXPTreePart Special
hi def link PATHS_EXPTreePartFile Type
hi def link PATHS_EXPTreeFile Normal
hi def link PATHS_EXPTreeExecFile Title
hi def link PATHS_EXPTreeDirSlash Identifier
hi def link PATHS_EXPTreeClosable Type

hi def link PATHS_EXPTreeBookmarksHeader statement
hi def link PATHS_EXPTreeBookmarksLeader ignore
hi def link PATHS_EXPTreeBookmarkName Identifier
hi def link PATHS_EXPTreeBookmark normal

hi def link PATHS_EXPTreeHelp String
hi def link PATHS_EXPTreeHelpKey Identifier
hi def link PATHS_TITLE         Type
hi def link PATHS_EXPTreeHelpCommand Identifier
hi def link PATHS_EXPTreeHelpTitle Macro
hi def link PATHS_EXPTreeToggleOff WarningMsg

hi def link PATHS_EXPTreeDir Normal
hi def link PATHS_EXPTreeUp Directory
hi def link PATHS_EXPTreeCWD Statement
hi def link PATHS_EXPTreeDirName Define
hi def link PATHS_EXPTreeOpenable Title
hi def link PATHS_EXPTreeFlag ignore
hi def link PATHS_EXPTreeRO WarningMsg
hi def link PATHS_EXPTreeBookmark Statement

hi def link PATHS_EXPFileTypeJS Statement
hi def link PATHS_EXPFileTypeHtml Type
hi def link PATHS_EXPFileTypeC Identifier
hi def link PATHS_EXPFileTypePy Function
hi def link PATHS_EXPFileTypeLua  Question
hi def link PATHS_EXPFileTypeSh Tag
hi def link PATHS_EXPFileTypeH Tag
hi def link Folded Normal


hi CursorLine  ctermbg=40

runtime syntax/frainuilist.vim

"hi Cursor ctermfg=fg ctermbg=bg guifg=None guibg=None















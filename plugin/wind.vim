"导入python plugin"
let s:script_folder_path = escape(expand('<sfile>:p:h' ), '\')

" 如果是 C 项目的情况下, 用于保存头文件所在的目录
" 使用 vim 接口是为了方便与其它的项目进行数据交换
let g:frain_include_dirs = ''

"------------------------------ python -----------------------------------------
python <<EOF
import sys
import os.path as path
import vim

dirname = path.dirname
join    = path.join

sys.path.insert(0, join(dirname(vim.eval('s:script_folder_path')), 'wind'))

from wind import IM
EOF
"-------------------------------------------------------------------------------

function! Input_Monitor(tp, key)
    py IM("key", vim.eval("a:tp"), vim.eval("a:key"))
    return ''
endfunction

set omnifunc="wind#Prompt"
"auto CursorHold   * py IM('event', "CursorHold")
"auto CursorHoldI  * py IM('event', "CursorHoldI")
auto CompleteDone * py IM("prompt", "done")

"map  <F4>          :ProjectSync<cr>
"map  <F6>          :Project<cr>

map  <F2>          :update<cr>
imap <F2>          <esc>:update<cr>
map  <F7>          <esc>:MarkTo<cr>
imap <F7>          <esc>:MarkTo<cr>
map  <F9>          <esc>:TagJump<cr>
map  <F8>          <esc>:TagBack<cr>
map  <F10>         <esc>:FSearch<cr>
vmap  <F10>        <esc>:FSearch Sel<cr>
imap <F12>         <esc>:ProjectTerminal<cr><cr>
map  <F12>         <esc>:ProjectTerminal<cr><cr>
map  <2-LeftMouse> <esc>:MarkTo<cr>
map  <C-w>o        <esc>:ClearAllWin<cr>
vmap w=            <esc>:silent Align<cr>
imap <F11>         <esc>:GotoInc<cr>
map  <F11>         <esc>:GotoInc<cr>
imap <C-s>         <esc>:SameWord<cr>a
map  <tab>         :py IM("frainui", "focus", "frain")<CR>
map *              viw""y/<C-R>0<CR>
vnoremap /         ""y/<C-R>0<CR>
map gf             :FileFilter<cr>

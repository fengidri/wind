"导入python plugin"
let s:script_folder_path = escape(expand('<sfile>:p:h' ), '\')

" 如果是 C 项目的情况下, 用于保存头文件所在的目录
" 使用 vim 接口是为了方便与其它的项目进行数据交换
let g:frain_include_dirs = ''
" code  mode call ycm timer
" let let key key ss ssss  s   s
let g:wind_im_timer_complete = 600
let g:wind_im_wubi = 0

"------------------------------ python -----------------------------------------
py3 <<EOF
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
    py3 IM("key", vim.eval("a:tp"), vim.eval("a:key"))
    return ''
endfunction

set omnifunc="wind#Prompt"
"CursorHold default timer out is 4000ms and this value also used for swap
"auto CursorHold   * py IM('event', "CursorHold")
"auto CursorHoldI  * py IM('event', "CursorHoldI")
auto CompleteDone * py3 IM("prompt", "done")

"map  <F4>          :ProjectSync<cr>
"map  <F6>          :Project<cr>

map  <F2>          :update<cr>
imap <F2>          <esc>:update<cr>
map  <F7>          <esc>:MarkTo<cr>
imap <F7>          <esc>:MarkTo<cr>
map  <F10>         <esc>:FSearchX<cr>
vmap <F10>         <esc>:FSearchX Sel<cr>
imap <F12>         <esc>:ProjectTerminal<cr><cr>
map  <F12>         <esc>:ProjectTerminal<cr><cr>
map  <2-LeftMouse> <esc>:MarkTo<cr>
map  <C-w>o        <esc>:ClearAllWin<cr>
vmap w=            <esc>:silent Align<cr>
imap <F11>         <esc>:GotoInc<cr>
map  <F11>         :GotoInc<cr>
imap <C-s>         <esc>:SameWord<cr>
map <C-s>          :SameWord<cr>a
map  <tab>         :py3 IM("frainui", "OP-Focus", "frain")<CR>
map *              viw""y/<C-R>0<CR>
map <F5>           <esc>:Run<CR>
inoremap <C-f>     <esc>:CFunComment<cr>
inoremap <C-h>     /*  */<esc>hhi

vnoremap /         ""y/<C-R>0<CR>

map gf             :GoAny file<cr>
map gt             :GoAny tag file<cr>
map tt             :GoAny tag all<cr>

map  <F9>          :GoAny tag jump<cr>
map  <F8>          :GoAny tag back<cr>
map  gh            :GoAny tag jump<cr>
map  gb            :GoAny tag back<cr>
"map  O             :Zoom<cr>




if has("gui_running")
else
    vnoremap "+y     y:MacClipPost<cr>
    map "+p      :MacClipGet<cr>p
endif


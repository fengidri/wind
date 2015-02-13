"导入python plugin"
"
let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

python <<EOF
import sys
import os
import vim

"增加基础python lib 路径, 增加pyplugin 路径"

# add paths
root = os.path.dirname(vim.eval('s:script_folder_path'))
pylib_path    = os.path.join(root, 'vimlib' )
pyplugin_path = os.path.join(root, "pyplugin" )
sys.path.insert( 0, pylib_path )
sys.path.insert( 0, pyplugin_path )

#load plugin
import pyvim
pyvim.load_plugin( pyplugin_path )

#init im
from im import Input_Monitor
IM = Input_Monitor.Input_Monitor( )
IM.init_monitor_keys( )
EOF

function! Input_Monitor( key )
    py IM.in_key( vim.eval("a:key"))
    return ''
endfunction

map  <F2>          :update<cr>
imap <F2>          <esc>:update<cr>
map  <F7>          <esc>:MarkTo<cr>
imap <F7>          <esc>:MarkTo<cr>
map  <F9>          <esc>:TagJump<cr>
map  <F8>          <esc>:TagBack<cr>
map  <F10>         <esc>:FSearch<cr>
imap <F12>         <esc>:!xterm&<cr><cr>
map  <F12>         <esc>:!xterm&<cr><cr>
map  <2-LeftMouse> <esc>:MarkTo<cr>
map  <C-w>o        <esc>:ClearAllWin<cr>
vmap w=            <esc>:silent Align<cr>
imap <F11>         <esc>:GotoInc<cr>
map  <F11>         <esc>:GotoInc<cr>

map  <F4>          :ProjectSync<cr>
map  <tab>         :PathsExpGo<cr>
map  <F6>          :Project<cr>

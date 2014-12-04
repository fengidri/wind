autocmd VimEnter  * call   input_monitor#Enable( )
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
imap  <F11>      <esc>:GotoInc<cr>
map   <F11>      <esc>:GotoInc<cr>

map <F4>         :ProjectSync<cr>
map <tab>        :PathsExpGo<cr>

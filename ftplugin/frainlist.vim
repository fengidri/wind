map <buffer> <cr>          :py IM("frainui", "open")<CR>
map <buffer> <2-LeftMouse> :py IM("frainui", "open")<CR>
map <buffer> o             :py IM("frainui", "open")<CR>
map <buffer> <bs>          :py IM("frainui", "close")<CR>
map <buffer> R             :py IM("frainui", "refresh")<CR>
map <buffer> dd            :py IM("frainui", "delete")<CR>
map <buffer> <tab>         :wincmd p<cr>

"map <buffer> H :FrainFilter<CR>
let b:frain_status_path = 'root'
setlocal statusline=%{b:frain_status_path}
setlocal cursorline
setlocal foldmethod=manual
setlocal foldminlines=0
setlocal foldlevelstart=14

setlocal buftype=nofile
setlocal noswapfile

setlocal fillchars=
setlocal conceallevel=3
setlocal concealcursor=nvic
setlocal winfixwidth
setlocal foldmethod=expr
setlocal foldexpr=0





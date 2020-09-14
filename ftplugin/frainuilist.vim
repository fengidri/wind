map <buffer> <cr>          :py3 IM("frainui", "OP-Open")<CR>
map <buffer> <2-LeftMouse> :py3 IM("frainui", "OP-Open")<CR>
map <buffer> o             :py3 IM("frainui", "OP-Open")<CR>
map <buffer> <bs>          :py3 IM("frainui", "OP-Close")<CR>
map <buffer> R             :py3 IM("frainui", "OP-Refresh")<CR>
map <buffer> dd            :py3 IM("frainui", "OP-Delete")<CR>
map <buffer> <tab>         :wincmd p<cr>
map <buffer> i j
map <buffer> s j
map <buffer> a j

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



setlocal nonumber



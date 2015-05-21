map <buffer> <cr> :FrainOpen<cr>
map <buffer> o :FrainOpen<cr>
map <buffer> <2-LeftMouse> :FrainOpen<CR>
map <buffer> <bs>  :FrainClose<CR>
map <buffer> H :FrainFilter<CR>
map <buffer> R :FrainRefresh<CR>
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





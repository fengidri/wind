map <buffer> <cr>          :py IM("frainui", "list-open")<CR>
map <buffer> o             :py IM("frainui", "list-open")<CR>
map <buffer> <2-LeftMouse> :py IM("frainui", "list-open")<CR>
map <buffer> <bs>          :py IM("frainui", "list-close")<CR>
map <buffer> R             :py IM("frainui", "list-refresh")<CR>

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





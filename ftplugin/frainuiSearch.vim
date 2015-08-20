setlocal conceallevel=3
setlocal concealcursor=nvic

"setlocal cursorline

setlocal buftype=nofile
setlocal noswapfile
set nonumber
map <buffer> <CR>  :py IM('frainui', 'OP-Active')<cr>

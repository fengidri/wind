setlocal conceallevel=3
setlocal concealcursor=nvic

"setlocal cursorline

setlocal buftype=nofile
setlocal noswapfile
set nonumber
map <CR>  :py IM('frainui', 'search_active')<cr>

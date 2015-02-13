"vimlib 中用于辅助的vim script"


"""""""""""""""""""""""""""""""""""SelMenu"""""""""""""""""""""""""""""""""""
"函数中用于传递返回数据的变量"
"let g:omniresult= []
"let g:omnicol = 0

"补全回调函数"
function! vimlib#SelMenuFunction( findstart, base )
  if a:findstart
      return g:omnicol
  else
      return g:omniresult
  endif
endfunction

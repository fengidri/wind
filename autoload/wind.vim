"vimlib 中用于辅助的vim script"


"""""""""""""""""""""""""""""""""""SelMenu"""""""""""""""""""""""""""""""""""
"函数中用于传递返回数据的变量"
"let g:omniresult= []
"let g:omnicol = 0

"补全回调函数"

function! wind#Prompt(findstart, base)
  if a:findstart
      py IM('prompt', 'findstart')
      return g:omnicol
  else
      py IM('prompt', 'base', vim.eval('a:base'))
      return g:omniresult
  endif
endfunction

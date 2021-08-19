"vimlib 中用于辅助的vim script"


"""""""""""""""""""""""""""""""""""SelMenu"""""""""""""""""""""""""""""""""""
"函数中用于传递返回数据的变量"
let g:omniresult= []
let g:omnicol = 0
let g:wind_commands_complete = []
"补全回调函数"
"
let s:invoke_other_fun = 0
let g:wind_with_ycm = -4

function! wind#Prompt(findstart, base)
    if a:findstart
        py3 IM('prompt', 'findstart')
        return g:omnicol
    else
        py3 IM('prompt', 'base', vim.eval('a:base'))
        " sjust call this when prompt out
        call feedkeys( "\<C-P>", 'n' )
        return g:omniresult
    endif
endfunction

function! wind#CommandsComplete(A, L, P)
    py3 pyvim.command_complete(vim.eval("a:A"), vim.eval("a:L"), vim.eval("a:P"))
    return g:wind_commands_complete
endfunction

function! wind#TimerHandler(id)
    py3 pyvim.timercall(vim.eval("a:id"))
endfunction

function! wind#py_load(name, path)
    let s:script_folder_path = escape(a:path, '\')
    py3 wind.load_plugin(vim.eval('a:name'), vim.eval('s:script_folder_path'))
endfunction

func! wind#popup_filter(winid, key)
    let s:l = split(a:key, '\zs')
    let s:key = []

    for k in s:l
        call add(s:key, char2nr(k))
    endfor

    py3 IM('popup')
    return 1
endfunc

python<<EOF
import sys
import os
from im import Input_Monitor
EOF

let g:omniresult= []

function! input_monitor#OmniComplete( findstart, base )
  if a:findstart
      return col( '.' )
  else

      return g:omniresult
  endif
endfunction

function input_monitor#Input_Monitor( key )
    py im.in_key( vim.eval("a:key"))
    return ''
endfunction
 
function input_monitor#Enable( )
    py im= Input_Monitor.Input_Monitor( )
    py im.init_monitor_keys( )

    py im.filetype()
    autocmd FileType,BufEnter * py im.filetype( )
endfunction

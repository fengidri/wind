python<<EOF
import sys
import os
from im import Input_Monitor
EOF



"对于每一个输入key的map 回调函数"
function input_monitor#Input_Monitor( key )
    py im.in_key( vim.eval("a:key"))
    return ''
endfunction
 
"input monitor main函数"
function input_monitor#Enable( )
    py im= Input_Monitor.Input_Monitor( )
    py im.init_monitor_keys( )

    "py im.filetype()
    "autocmd FileType,BufEnter * py im.filetype( )
endfunction

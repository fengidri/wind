"导入python plugin"
"
let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )
python <<EOF
import sys
import os
import vim

"增加基础python lib 路径, 增加pyplugin 路径"


root = os.path.dirname(vim.eval('s:script_folder_path'))
pylib_path    = os.path.join(root, 'vimlib' )
pyplugin_path = os.path.join(root, "pyplugin" )
sys.path.insert( 0, pylib_path )
sys.path.insert( 0, pyplugin_path )

import pyvim
pyvim.load_plugin( pyplugin_path )
EOF

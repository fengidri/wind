import vim
import pyvim
import re
import os

@pyvim.cmd()
def GotoInc( ):
    types = { 'c':['h'], 'h':['c', 'cpp', 'cc' ], 'cpp':['h'] , 'cc': ['h']}
    target_types = [  ]

    match = re.search('#include\s+["<](.+)[>"]', pyvim.getline( ))
    if match:
        target_files = [match.group( 1 )]
    else:
        target_files = [  ]
        base_name = os.path.basename( vim.current.buffer.name )
        model_name = base_name.split( '.' )[ 0 ]
        model_type = base_name.split( '.' )[ 1 ]

        target_types = types.get(model_type)
        if not target_types:
            return

        for t in target_types:
            target_files.append( model_name + '.' + t )


    root = pyvim.get_cur_root()
    if not root:
        return

    for root, dirs, files in os.walk( root ):
        for target_file in target_files:
            if target_file in files:
                target_path = os.path.join( root, target_file )
                pyvim.gotofile( target_path )
                return 0
    pyvim.log.info( 'not find the file:%s'% target_file )

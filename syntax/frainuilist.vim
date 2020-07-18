syntax match Index "^\d\+," conceal cchar=.

"use for color set in py"
syntax match FrainUiSig "\\red;"   conceal cchar=\   contained
syntax match FrainUiSig "\\blue;"  conceal cchar=\   contained
syntax match FrainUiSig "\\green;" conceal cchar=\   contained
syntax match FrainUiSig "\\end;"   conceal cchar=\   contained

syntax match FrainUIRed   "\\red;.*\\end;"   contains=FrainUiSig
syntax match FrainUIBlue  "\\blue;.*\\end;"  contains=FrainUiSig
syntax match FrainUIGreen "\\green;.*\\end;" contains=FrainUiSig

hi FrainUIRed   guifg=red
hi FrainUIBlue  guifg=blue
hi FrainUIGreen guifg=green

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

syn keyword	cType		u32 u64 u8 u16 __be32
syn keyword	cType		__be32 __be16 __be8 __be64
syn keyword	cType		__le32 __le16 __le8 __le64
syn keyword	cType		struct
syn keyword	cType		int int32 int64

syn keyword cLabel f
syn keyword cRepeat m s

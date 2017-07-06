# Wind
基于python 的vim 插件框架. 提供一套灵活方便的插件框架. 并完成一些核心的功能.

# feautre

* wubi 输入法
* 输入监控
* 路径补全
* YouCompleteMe 支持
* 目录浏览
* 工程管理
* 源码信息
* 头文件与源码切换
* 符号跳转
* 当然 word hlight
* git 分支显示
* vim python 库
* vim python ui 库




# pyvim

* pyvim.Roots: current path root list. just work in the context of frain.
* pyvim.echo(msg, hl=bool):  echo msg to vim msg line.
* pyvim.addevent(event, cb): bind cb callback to the vim events.
    * BufEnter

# frain


# vim
* vim.command(cmd): run vim ex cmd




# frainui

* frainui.LIST(title, cb): make tree list window. cb is the callback to generate the list.
 return list object. cb function: `def cb(node, win):`. the node is the root
 node of the list window.
* frainui.Leaf(name, ctx=None, handle=None, diskplay=None): create tree leaf of the tree list.
    * name: leaf name
    * ctx: ctx
    * handle: call back when user select the leaf. 

## frainui list object
* show(): open the tree list window.
* refresh(): refresh the list node in the list window. This function will call
  the cb trans by frainui.LIST.
* FREventBind(event, cb): bind the cb callback to the event point. the event
  has this:
  * ListReFreshPre



## frainui.LIST


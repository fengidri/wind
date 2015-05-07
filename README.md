# pyplugin
基于python 的vim 插件框架. 提供一套灵活方便的插件框架. 并完成一些核心的功能.

## vimlib
插件的core. 这部份提供许多python接口. 这些接口是对于vim 的接口的封装. 
同时也提供了一个插件机制. 可以方便地增加新命令与事件. 

同时还重点提供两个功能. vuirpc与im. 

im的实质上是一个对于vim 所有的输入的监控. 并定制这些输入的结果. 在这之上实现了一
个五笔输入法. 

vuirpc 是一个网络交互实现. 用于与vuirpc\_server 进行连接.
vuirpc\_server 提供一个gui 操作实现. 可以大大扩展用户的操作.

## pyplugin
用于保存python 编写的插件, 所有的插件只要按格式编写, 放到这个目录下可以工作.

详细的说明: [the vim plugin of fengidri](http://blog.fengidri.me/?id=1761857)



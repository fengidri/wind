# input\_monitor
这个类的im方法是im的入口. 会根据当前的文件类型查找对应的inputer.
如果没有找到就直接输入.


# filetype
所有的filetype都是继承自imutils中的filetype. im方法由input\_monitor进行调用.
继承的类要在初始化的时候通过im\_append顺序增加inputer.

im\_ft是filetype的一个list属性. 这个属性记录了类适用于哪些filetype.



# inputer
所有的inputer都在目录inputers下. 对应的类要在__init__中进行注册. 
所有的inputer 类的im 方法是对应的入口. 

一般而言inputer 要对于当前的环境进行检查, 如果不适用于当前的inputer
则返回False. im会调用下一个inputer.



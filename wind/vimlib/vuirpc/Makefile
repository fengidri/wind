SrcFiles=$(wildcard rnetwork/ae.c rnetwork/anet.c rnetwork/zmalloc.c  \
		 cJSON/cJSON.c rlist/*.c rstr/*.c client.c gtklist.c network.c\
		 quick_search.c vuiint.c vuirpc.c so.c) 
Objs=$(SrcFiles:.c=.o)
Include=-Icjson -Irnetwork -Irstr -Irlist `pkg-config --cflags gtk+-3.0`
all:$(Objs)
	gcc $(Objs)  -o vuirpc_server -lm `pkg-config --libs gtk+-3.0` -pthread

$(Objs):%.o:%.c
	gcc -g -c $(Include) $< -o $@ -fPIC

clean:
	@find . \
	        \( -name '*.[os]' \
			-o -name '*.ko' \
			-o -name '.*.cmd' \
	        -o -name '*.d'\
			-o -name '.*.tmp'\
			-o -name '*.mod.c' \
	        -o -name '*.symtypes'\
			-o -name 'modules.order' \
	        -o -name 'Module.markers' \) \
	        -type f -print | xargs rm -f
	@-rm -f $(Target)
	@-rm -f $(LN_NAME)
	@-rm -f $(Pack_Name)
	@echo -e "___________________________________________________________"
	@echo "clean completed!"

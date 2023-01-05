CFLAGS += -Werror -Wall

looter.so: looter.c
	gcc $(CFLAGS) -fPIC -shared -Xlinker -x -o $@ $< -lcurl


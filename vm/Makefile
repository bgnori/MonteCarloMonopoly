
all: libmvm.so unittest libqueue.so

val: unittest
	LD_LIBRARY_PATH=. valgrind ./unittest

test: unittest
	LD_LIBRARY_PATH=. ./unittest

clean:
	rm libmvm.so; rm unittest; rm mvm.o; rm libqueue.so; rm libqueue.o

unittest: unittest.o libmvm.so libqueue.so
	gcc unittest.o -L. -lmvm -lqueue -o unittest

unittest.o : mvm.h unittest.c libqueue.so
	gcc -std=c99 -Wall -c unittest.c

libmvm.so: mvm.o
	gcc -shared -Wl,-soname,libmvm.so -o libmvm.so mvm.o

mvm.o: mvm.h mvm.c
	gcc -fPIC -std=c99 -Wall -c mvm.c


libqueue.so: queue.o
	gcc -shared -Wl,-soname,libqueue.so -o libqueue.so queue.o

queue.o: queue.h queue.c
	gcc -fPIC -std=c99 -Wall -c queue.c


all: libmvm.so unittest libqueue.so

run: runner
	LD_LIBRARY_PATH=. ./runner

val: unittest
	LD_LIBRARY_PATH=. valgrind ./unittest

test_all: test_mvm test_loader

test_loader: unittest_loader
	LD_LIBRARY_PATH=. ./unittest_loader

test_mvm: unittest_mvm
	LD_LIBRARY_PATH=. ./unittest_mvm

clean:
	rm *.so; rm unittest_mvm; rm unittest_loader; rm *.o; rm libqueue.so

runner: runner.o libmvm.so libqueue.so
	gcc runner.o -L. -lmvm -lqueue -o runner

unittest_mvm: unittest_mvm.o libmvm.so libqueue.so libunittest.so 
	gcc unittest_mvm.o -L. -lmvm -lqueue -lunittest -o unittest_mvm

unittest_mvm.o : mvm.h unittest_mvm.c libqueue.so
	gcc -std=c99 -Wall -c unittest_mvm.c

unittest_loader: unittest_loader.o libmvm.so libqueue.so libunittest.so
	gcc unittest_loader.o -L. -lmvm -lqueue -lunittest -o unittest_loader

unittest_loader.o : mvm.h unittest_loader.c libqueue.so loader.h
	gcc -std=c99 -Wall -c unittest_loader.c


runner.o : mvm.h runner.c libqueue.so
	gcc -std=c99 -Wall -c runner.c

libmvm.so: mvm.o loader.o
	gcc -shared -Wl,-soname,libmvm.so -o libmvm.so mvm.o loader.o

libunittest.so: unittest.o
	gcc -shared -Wl,-soname,libunittest.so -o libunittest.so unittest.o

unittest.o: unittest.h unittest.c
	gcc -fPIC -std=c99 -Wall -c unittest.c

mvm.o: mvm.h mvm.c
	gcc -fPIC -std=c99 -Wall -c mvm.c

loader.o: mvm.h loader.c loader.h
	gcc -fPIC -std=c99 -Wall -c loader.c

libqueue.so: queue.o
	gcc -shared -Wl,-soname,libqueue.so -o libqueue.so queue.o

queue.o: queue.h queue.c
	gcc -fPIC -std=c99 -Wall -c queue.c

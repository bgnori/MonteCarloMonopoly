
all: libmvm.so runner libqueue.so

run: runner
	LD_LIBRARY_PATH=. ./runner

clean:
	rm libmvm.so; rm runner; rm mvm.o; rm libqueue.so; rm libqueue.o

runner: runner.o libmvm.so libqueue.so
	gcc runner.o -L. -lmvm -lqueue -o runner

runner.o : mvm.h runner.c libqueue.so
	gcc -std=c99 -Wall -c runner.c

libmvm.so: mvm.o
	gcc -shared -Wl,-soname,libmvm.so -o libmvm.so mvm.o

mvm.o: mvm.h mvm.c
	gcc -fPIC -std=c99 -Wall -c mvm.c


libqueue.so: queue.o
	gcc -shared -Wl,-soname,libqueue.so -o libqueue.so queue.o

queue.o: queue.h queue.c
	gcc -fPIC -std=c99 -Wall -c queue.c

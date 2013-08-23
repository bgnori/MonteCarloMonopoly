
all: libmvm.so runner

run: runner
	LD_LIBRARY_PATH=. ./runner

clean:
	rm libmvm.so; rm runner; rm mvm.o

runner: runner.o libmvm.so
	gcc runner.o -L. -lmvm -o runner

runner.o : mvm.h runner.c
	gcc -std=c99 -Wall -c runner.c

libmvm.so: mvm.o
	gcc -shared -Wl,-soname,libmvm.so -o libmvm.so mvm.o

mvm.o: mvm.h mvm.c
	gcc -fPIC -std=c99 -Wall -c mvm.c



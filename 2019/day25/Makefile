CC=clang

CFLAGS = -g -Wall -Wextra -O3
INC = -I../intcode
# DEFINES = -DENABLE_TRACE

.PHONY: all
all: part1

%.o: %.c
	$(CC) $(INC) $(CFLAGS) $(DEFINES) -o $@ -c $<

part1: part1.o intcode.o
	$(CC) $(INC) -o $@ $^

intcode.o: ../intcode/intcode.c ../intcode/intcode.h
	$(CC) -c $(INC) $(CFLAGS) $(DEFINES) ../intcode/intcode.c

.PHONY: clean
clean:
	rm -f $(obj) part1 *.o

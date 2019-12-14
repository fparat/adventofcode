CC=gcc

LDFLAGS = -lncurses
INC = -I../intcode

.PHONY: all
all: part1 part2

%.o: %.c
	$(CC) $(INC) $(CFLAGS) -o $@ -c $<

part1: part1.o intcode.o
	$(CC) $(INC) -o $@ $^

part2: part2.o intcode.o
	$(CC) $(INC) -o $@ $^ $(LDFLAGS)

intcode.o:
	$(CC) -c $(INC) ../intcode/intcode.c

.PHONY: clean
clean:
	rm -f $(obj) part1 part2 *.o

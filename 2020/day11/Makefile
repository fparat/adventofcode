CC=clang

.PHONY: all
all: part1 part2

%.o: %.c
	$(CC) $(INC) $(CFLAGS) -o $@ -c $<

part1: part1.o
	$(CC) $(INC) -o $@ $^

part2: part2.o
	$(CC) $(INC) -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f $(obj) part1 part2 *.o

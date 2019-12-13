src = $(wildcard *.c)
obj = $(src:.c=.o)

.PHONY: run_test
run_test: test
	@./test

test: $(obj)
	$(CC) -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f $(obj) test

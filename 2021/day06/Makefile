RUSTC=rustc
RUSTFLAGS = -g -O

%: %.rs
	$(RUSTC) $(RUSTFLAGS) -o $@ $<

.PHONY: all
all: part1 part2

.PHONY: clean
clean:
	rm -f part1 part2

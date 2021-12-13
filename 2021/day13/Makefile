RUSTC=rustc
RUSTFMT=rustfmt
RUSTFLAGS = -g -O --edition 2021

%: %.rs
	$(RUSTC) $(RUSTFLAGS) -o $@ $<

.PHONY: all
all: part1 part2

.PHONY: fmt
fmt:
	$(RUSTFMT) *.rs

.PHONY: clean
clean:
	rm -f part1 part2

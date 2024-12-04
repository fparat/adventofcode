RUSTC=rustc
RUSTFLAGS = -g -O

%: %.rs
	$(RUSTC) $(RUSTFLAGS) -o $@ $<

test_%: %.rs
	$(RUSTC) $(RUSTFLAGS) --test -o $@ $<

.PHONY: all
all: part1 part2

.PHONY: clean
clean:
	rm -f part1 part2

.PHONY: fmt
fmt:
	rustfmt --edition 2021 *.rs

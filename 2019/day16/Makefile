RUSTC=rustc
RUSTFLAGS = -g -O

%: %.rs
	$(RUSTC) $(RUSTFLAGS) -o $@ $<

test_%: %.rs .FORCE
	$(RUSTC) $(RUSTFLAGS) --test -o $@ $<
	./$@

.PHONY: all
all: part1 part2

.PHONY: clean
clean:
	rm -f part1 part2

.PHONY: .FORCE
.FORCE:

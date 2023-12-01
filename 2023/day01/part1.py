#!/usr/bin/env python3

# attempt of minimalist shell command
#   cat input | python3 -c 'import sys;print(...)'
import sys;print(sum(map(lambda c:int(c[0]+c[-1]),map(lambda l:list(filter(str.isdigit,l)),sys.stdin))))

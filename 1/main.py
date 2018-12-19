#!/usr/bin/env pypy3
from kitchen_sink import *

d = { 0: 1 }
l = list(int(l) for l in input_lines())

current = 0
found = False
while not found:
    print("loop.")
    for v in l:
        current += v
        d[current] = d.get(current, 0) + 1
        if d[current] == 2:
            print("Found! %s" % current)
            found = True
            break
    
        
    

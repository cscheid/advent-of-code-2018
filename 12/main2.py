import sys
from collections import defaultdict
import time

def parse_input(ls):
    initial_state = next(ls).strip().split(' ')[2]
    next(ls)
    result = [0] * 32
    d = defaultdict(int)
    for i, c in enumerate(initial_state):
        if c == '#':
            d[i] = 1
    try:
        while True:
            l = next(ls)
            l = l.strip().split()
            rule = 0
            for i, v in enumerate(l[0]):
                k = 1 << i
                if v == '#':
                    rule += k
            result[rule] = 1 if l[2] == '#' else 0
    except StopIteration:
        return (d, result)

def make_pattern(*lst):
    return "".join('#' if i == 1 else '.' for i in lst)

def print_pattern(d):
    vmin = min(d.keys())
    vmax = max(d.keys())
    return "".join(['#' if d[i] == 1 else '.' for i in range(vmin, vmax+1)])

def step(d, rules):
    result = defaultdict(int)
    vmin = min(d.keys())
    vmax = max(d.keys())
    for i in range(vmin-2, vmax+3):
        rule = 0
        for j in range(5):
            rule += ((1 << j) if d[i+j-2] == 1 else 0)
        if rules[rule] == 1:
            result[i] = 1
    return result

state, rules = parse_input(i for i in sys.stdin.readlines())

prev_time = time.time()

for i in range(500000):
    prev_time = time.time()
    for j in range(100000):
        state = step(state, rules)
    cur_time = time.time()
    print("\r                   \r%d, %s" % ((i * 100000), cur_time - prev_time))

print(sum(i if c == 1 else 0 for i,c in state.items()))
 

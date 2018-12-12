import sys
from collections import defaultdict

def parse_input(ls):
    initial_state = next(ls).strip().split(' ')[2]
    next(ls)
    result = defaultdict(int)
    result = [0] * 32
    d = defaultdict(int)
    for i, c in enumerate(initial_state):
        if c == '#':
            d[i] = 1
    try:
        while True:
            l = next(ls)
            l = l.strip().split()
            result
            result[l[0]] = l[2]
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
        pattern = make_pattern(*(d[v] for v in range(i-2, i+3)))
        if rules[pattern] == '#':
            result[i] = 1
    return result

state, rules = parse_input(i for i in sys.stdin.readlines())

for i in range(50000000000):
    state = step(state, rules)
    if i % 10000 == 0:
        print("\r                   \r%d" % i)

print(sum(i if c == 1 else 0 for i,c in state.items()))
 

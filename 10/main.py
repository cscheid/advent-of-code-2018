import re
import sys
from collections import defaultdict

r = re.compile(r'position=< *(-?[0-9]+), *(-?[0-9]+)> velocity=< *(-?[0-9]+), *(-?[0-9]+)>')
def parse_point(v):
    return list(int(i) for i in r.match(v).groups())

def state_at(l, t):
    return list((v[0] + t * v[2], v[1] + t * v[3]) for v in l)

def board_area(l):
    min_x = min(v[0] for v in l)
    min_y = min(v[1] for v in l)
    max_x = max(v[0] for v in l)
    max_y = max(v[1] for v in l)
    return (max_y - min_y) * (max_x - min_x)

def print_board(l):
    min_x = min(v[0] for v in l)
    min_y = min(v[1] for v in l)
    max_x = max(v[0] for v in l)
    max_y = max(v[1] for v in l)
    b = []
    print(min_x, max_x, min_y, max_y)
    for i in range(max_y - min_y + 1):
        b.append(['.'] * (max_x - min_x + 1))
    for p in l:
        b[p[1]-min_y][p[0]-min_x] = '#'
    for row in b:
        print("".join(row))

def min_area(l):
    current_area = board_area(state_at(l, 0))
    print(0, current_area)
    t = 1
    next_board = state_at(l, t)
    next_area = board_area(next_board)
    print(t, next_area)
    while next_area < current_area:
        current_area = next_area
        t += 1
        next_board = state_at(l, t)
        next_area = board_area(next_board)
        print("\r                             \r%s %s" % (t, next_area), end='')
    print()
    return t

if __name__ == '__main__':
    l = list(parse_point(v) for v in sys.stdin.readlines())
    print_board(state_at(l, 10086))
    # print("min area: %s", min_area(l))
    # exit(1)
    # print_board(state_at(l, 0))
    # print()
    # print_board(state_at(l, 1))
    # print()
    # print_board(state_at(l, 2))
    # print()
    # print_board(state_at(l, 3))
    # print()
    

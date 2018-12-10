import re
import sys

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
    for i in range(max_y - min_y + 1):
        b.append(['.'] * (max_x - min_x + 1))
    for p in l:
        b[p[1]-min_y][p[0]-min_x] = '#'
    for row in b:
        print("".join(row))

def min_area(l):
    current_area = board_area(state_at(l, 0))
    t = 1
    next_board = state_at(l, t)
    next_area = board_area(next_board)
    while next_area < current_area:
        current_area = next_area
        t += 1
        next_board = state_at(l, t)
        next_area = board_area(next_board)
        if t % 1000 == 0:
            print("\r                             \r%s %s" % (t, next_area), end='')
    print()
    return t-1

def min_variation(l):
    n = len(l)
    a = sum(v[0] * v[2] for v in l)
    b = sum(v[2] * v[2] for v in l)
    c = sum(v[0] for v in l)
    d = sum(v[2] for v in l)
    e = sum(v[1] * v[3] for v in l)
    f = sum(v[3] * v[3] for v in l)
    g = sum(v[1] for v in l)
    h = sum(v[3] for v in l)
    v1 = (n * (n-1) * b - n * d * d) + (n * (n-1) * f - n * h * h)
    v2 = (n * (n-1) * a - (n-1) * c * d) + (n * (n-1) * e - (n-1) * g * h)
    return -v2/v1

if __name__ == '__main__':
    l = list(parse_point(v) for v in sys.stdin.readlines())
    s1 = round(min_variation(l))
    s2 = min_area(l)
    print(s1)
    print(s2)
    print_board(state_at(l, 10086))
    

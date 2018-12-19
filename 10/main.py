#!/usr/bin/env python3

from kitchen_sink import *
import re
import sys
import numpy as np

r = re.compile(r'position=< *(-?[0-9]+), *(-?[0-9]+)> velocity=< *(-?[0-9]+), *(-?[0-9]+)>')
def parse_point(v):
    l = list(int(i) for i in r.match(v).groups())
    p = np.array([l[0], l[1]])
    v = np.array([l[2], l[3]])
    return p, v

def state_at(l, t):
    return np.array(list(p + t * v for (p, v) in l))

def board_area(l):
    min_x = l[:,0].min()
    min_y = l[:,1].min()
    max_x = l[:,0].max()
    max_y = l[:,1].max()
    return (max_y - min_y) * (max_x - min_x)

def print_board(l):
    min_x = l[:,0].min()
    min_y = l[:,1].min()
    max_x = l[:,0].max()
    max_y = l[:,1].max()
    b = []
    for i in range(max_y - min_y + 1):
        b.append(['.'] * (max_x - min_x + 1))
    for p in l:
        b[p[1]-min_y][p[0]-min_x] = '#'
    for row in b:
        print("".join(row))

def min_area(l):
    def board_area_at(t):
        return board_area(state_at(l, t))
    a = 0
    b = 1000000 # or something else found by hand
    def done(c, d, fc, fd):
        return d-c < 0.1
    r = golden_section_minimization(a, b, board_area_at, done)
    return round(r)

def min_variation(l):
    n = len(l)
    a = (l[:,0,0] * l[:,1,0]).sum()
    b = (l[:,1,0] * l[:,1,0]).sum()
    c = l[:,0,0].sum()
    d = l[:,1,0].sum()
    e = (l[:,0,1] * l[:,1,1]).sum()
    f = (l[:,1,1] * l[:,1,1]).sum()
    g = l[:,0,1].sum()
    h = l[:,1,1].sum()
    v1 = (n * (n-1) * b - n * d * d) + (n * (n-1) * f - n * h * h)
    v2 = (n * (n-1) * a - (n-1) * c * d) + (n * (n-1) * e - (n-1) * g * h)
    return -v2/v1

if __name__ == '__main__':
    l = np.array(list(parse_point(v) for v in sys.stdin.readlines()))
    s1 = round(min_variation(l))
    print(s1)
    s2 = min_area(l)
    print(s2)
    print_board(state_at(l, 10086))
    

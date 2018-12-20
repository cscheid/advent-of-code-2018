#!/usr/bin/env pypy3
# 8:05AM
#  8:18AM
#  8:24AM

import sys
from kitchen_sink import *

f = Board(list(list(c for c in l.strip()) for l in sys.stdin.readlines())).sentinel('X')

def istree(c): return c == '|'
def islumberyard(c): return c == '#'

def step(board):
    w, h = board.dims()

    def decide_board(x, y, c):
        new_c = c
        if c == '.':
            trees = isize(filter(istree, board.adjacent8(x, y)))
            if trees >= 3:
                new_c = '|'
        elif c == '|':
            trees = isize(filter(islumberyard, board.adjacent8(x, y)))
            if trees >= 3:
                new_c = '#'
        elif c == '#':
            trees = isize(filter(islumberyard, board.adjacent8(x, y)))
            lumbs = isize(filter(istree, board.adjacent8(x, y)))
            if trees < 1 or lumbs < 1:
                new_c = '.'
        else:
            new_c = c
        return new_c
    
    return board.map(decide_board)

def value(board):
    trees = isize(filter(lambda p: p == '|', board.values()))
    lumbs = isize(filter(lambda p: p == '#', board.values()))
    return (trees, lumbs, trees * lumbs)

# 1496: 
# 1580: 184481
# 

# period = 84
# 1496 + k 84 = 1000000000
# k = (1000000000 - 1496) / 84

for i in range(1000000000):
    if i % 84 == 1504 % 84:
        print(value(f), i)
    f = step(f)


                

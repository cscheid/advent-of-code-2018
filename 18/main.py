#!/usr/bin/env pypy3
# 8:05AM
#  8:18AM
#  8:24AM

import sys
from kitchen_sink import *

f = input_board().sentinel('X')

def istree(c): return c == '|'
def islumberyard(c): return c == '#'

def step(board):
    def decide_board(x, y, c):
        if   c == '.' and  isize(filter(istree,       board.adjacent8(x, y))) >= 3:
            return '|'
        elif c == '|' and  isize(filter(islumberyard, board.adjacent8(x, y))) >= 3:
            return '#'
        elif c == '#' and (isize(filter(islumberyard, board.adjacent8(x, y))) < 1 or 
                           isize(filter(istree,       board.adjacent8(x, y))) < 1):
            return '.'
        else:
            return c
    return board.map(decide_board)

def value(board):
    trees = isize(filter(istree,       board.values()))
    lumbs = isize(filter(islumberyard, board.values()))
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


                

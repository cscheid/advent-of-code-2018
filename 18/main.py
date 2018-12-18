# 8:05AM
#  8:18AM
#  8:24AM

import sys

f = list(l.strip() for l in sys.stdin.readlines())

def adjacent(board, y, x):
    for i in range(y-1, y+2):
        if i < 0:
            continue
        if i >= len(board):
            continue
        for j in range(x-1, x+2):
            if j < 0:
                continue
            if j >= len(board[0]):
                continue
            if i == y and j == x:
                continue
            try:
                yield board[i][j]
            except IndexError:
                pass

def step(board):
    w = len(board[0])
    h = len(board[1])
    new_board = []
    for y in range(h):
        l = []
        for x in range(w):
            c = board[y][x]
            new_c = c
            if c == '.':
                trees = len(list(i for i in adjacent(board, y, x) if i == '|'))
                if trees >= 3:
                    new_c = '|'
            elif c == '|':
                trees = len(list(i for i in adjacent(board, y, x) if i == '#'))
                if trees >= 3:
                    new_c = '#'
            elif c == '#':
                trees = len(list(i for i in adjacent(board, y, x) if i == '#'))
                lumbs = len(list(i for i in adjacent(board, y, x) if i == '|'))
                if trees < 1 or lumbs < 1:
                    new_c = '.'
            else:
                raise Exception("unknown terrain %s" % c)
            l.append(new_c)
        new_board.append("".join(l))
    return new_board

def value(board):
    w = len(board[0])
    h = len(board)
    trees = 0
    lumbs = 0
    for i in range(h):
        for j in range(w):
            if board[i][j] == '|':
                trees += 1
            if board[i][j] == '#':
                lumbs += 1
    return (trees, lumbs, trees * lumbs)

def pprint(board):
    for b in board:
        print(b)
    print()

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


                

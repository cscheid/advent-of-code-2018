#!/usr/bin/env pypy3

from kitchen_sink import *

def parse_board(ls):
    return Board([[int(i) for i in l.split()] for l in ls])

def rect(board, x1, y1, x2, y2):
    return board[y1][x1] + board[y2][x2] - board[y1][x2] - board[y2][x1]

def find_greatest_3x3(board):
    w, h = board.dims()
    mx = -1000000000000
    argmax = None
    for i in range(0, w-2):
        for j in range(0, h-2):
            s = rect(board, i, j, i+3, j+3)
            if s > mx:
                mx = s
                argmax = ((i+1,j+1), (i+4, j+4))
    return mx, argmax

def find_greatest_square(board):
    w, h = board.dims()
    mx = -1000000000000
    argmax = None
    for k in range(1, w):
        for i in range(0, w-k):
            for j in range(0, h-k):
                s = rect(board, i, j, i+k, j+k)
                if s > mx:
                    mx = s
                    argmax = ((i+1,j+1), (i+k, j+k), k)
    return mx, argmax

serial_number = 3463
def make_board():
    result = []
    def power_level(x, y, _):
        x += 1
        y += 1
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial_number
        power_level *= rack_id
        power_level = int(power_level / 100) % 10
        power_level -= 5
        return power_level
    return Board.index(300, 300).map(power_level)

if __name__ == '__main__':
    sat = make_board().sat()
    print(find_greatest_square(sat))

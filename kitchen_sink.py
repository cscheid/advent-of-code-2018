import sys
from collections import defaultdict

def argmax(d, by=lambda v: v):
    try:
        enum = d.items()
    except AttributeError:
        enum = d
    current_max = None
    current_key = None
    for (k, v) in enum:
        value = by(v)
        if current_key is None or value > current_value:
            current_key = k
            current_value = value
            current_max = v
    return current_key, current_max

def histogram(w):
    result = defaultdict(int)
    for l in w:
        result[l] = result.get(l, 0) + 1
    return result

def group_by_count(w):
    result = histogram(w)
    inv = {}
    for (k, v) in result.items():
        inv.setdefault(v, []).append(k)
    return inv

def permutations(lst):
    if len(lst) == 0:
        yield []
    for i in range(len(lst)):
        rest = lst[:i] + lst[i+1:]
        for p in permutations(rest):
            yield [lst[i]] + p

def pairs(lst):
    return zip(lst, lst[1:])

def input_lines():
    result = list(l.strip('\n') for l in sys.stdin if l.strip('\n') != '')
    if len(result) == 0:
        raise Exception("EMPTY INPUT!")
    return result

##############################################################################
# 2d board stuff, or can i haz APL
#
# possibly should be called "2d_array", but board makes sense in aoc contexts

def constant_board(w, h, v):
    board = []
    for _ in range(h):
        board.append([v] * w)
    return board

def empty_board(w, h):
    return constant_board(w, h, 0)

def pprint_board(board):
    for l in board:
        for v in l:
            print("% 3d " % v, end='')
        print()

def add_board(board1, board2):
    return map_board(lambda a, b: a + b, board1, board2)

def map_board(f, *boards): # board1, board2):
    return list(list(f(*args) for args in zip(*largs))
                for largs in zip(*boards))

def index_board(w, h):
    board = []
    for y in range(h):
        line = []
        for x in range(w):
            line.append((x, y))
        board.append(line)
    return board

def sentinel_board(board, sentinel):
    w = len(board[0])
    result = []
    result.append([sentinel] * (w + 2))
    for l in board:
        result.append([sentinel] + l + [sentinel])
    result.append([sentinel] * (w + 2))
    return result


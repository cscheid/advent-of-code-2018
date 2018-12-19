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

def const(x):
    def f(_):
        return x
    return f

##############################################################################
# 2d board stuff, or can i haz APL
#
# possibly should be called "2d_array", but board makes sense in aoc contexts

class Board:

    # you should probably not use this
    def __init__(self, v):
        self.v = v

    def dims(self):
        v = self.v
        return (len(v[0]), len(v))

    @staticmethod
    def constant(w, h, v):
        board = []
        for _ in range(h):
            board.append([v] * w)
        return Board(board)

    @staticmethod
    def empty(w, h):
        return Board.constant(w, h, 0)

    def pprint(self):
        board = self.v
        for l in board:
            for v in l:
                print("% 3s " % (v,), end='')
            print()

    def map(self, f, *others): # board1, board2):
        boards = list(b.v for b in (self,) + others)
        return Board(list(list(f(*args) for args in zip(*largs))
                          for largs in zip(*boards)))

    @staticmethod
    def index(w, h):
        board = []
        for y in range(h):
            line = []
            for x in range(w):
                line.append((x, y))
            board.append(line)
        return Board(board)

    def sentinel(self, sentinel):
        board = self.v
        w = len(board[0])
        result = []
        result.append([sentinel] * (w + 2))
        for l in board:
            result.append([sentinel] + l + [sentinel])
        result.append([sentinel] * (w + 2))
        return result

    def keys(self):
        w, h = self.dims()
        for y in range(h):
            for x in range(w):
                yield (x, y)

    def values(self):
        w, h = self.dims()
        for l in self.v:
            yield from l

    def items(self):
        w, h = self.dims()
        for y in range(h):
            for x in range(w):
                yield (x, y, self.v[y][x])

    def __add__(self, other):
        return self.map(lambda a, b: a + b, other)

    def __sub__(self, other):
        return self.map(lambda a, b: a - b, other)

    def __getitem__(self, y):
        return self.v[y]
    
##############################################################################
# an ugly directed graph, represented as two dict of lists, one for out edges
# the other for inedges

def edges_to_graph(edges):
    d = {}
    d_inv = {}
    v_set = set()
    for (f, t) in edges:
        d.setdefault(f, []).append(t)
        d_inv.setdefault(t, []).append(f)
        v_set.add(f)
        v_set.add(t)
    for v in v_set:
        d.setdefault(v, [])
    return d, d_inv


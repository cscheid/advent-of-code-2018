import sys
from collections import defaultdict, deque

##############################################################################
# utils

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

def deque_top(d):
    v = d.popleft()
    d.appendleft(v)
    return v

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

class Graph:

    def __init__(self, edges):
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
        self.d = d
        self.d_inv = d_inv

    def vertices(self):
        return self.d.keys()

    def in_degree(self, k):
        return len(self.d_inv.get(k, []))

    def out_degree(self, k):
        return len(self.d.get(k, []))

    def sources(self):
        for k in self.d.keys():
            if self.in_degree(k) == 0:
                yield k
                
    def sinks(self):
        for k in self.d.keys():
            if self.out_degree(k) == 0:
                yield k

    def __contains__(self, k):
        return k in self.d

    def remove(self, f):
        for t in self.d[f]:
            self.d_inv[t].remove(f)
        del self.d[f]

    def topo_sort(self):
        d = self.d
        d_inv = self.d_inv
        sources = list(k for k in d.keys() if in_degree(d, d_inv, k) == 0)
        sources.sort(key=lambda k: -ord(k))
        result = []
        while len(sources):
            f = sources.pop()
            sources = list(v for v in sources if v != f)
            if f in d:
                for t in d[f]:
                    d_inv[t].remove(f)
                del d[f]
            result.append(f)
            sources.extend(list(k for k in d.keys() if in_degree(d, d_inv, k) == 0))
            sources.sort(key=lambda k: -ord(k))
        return result
        print("".join(result))

################################################################################
# simple n-ary tree

class Tree:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def pprint(self, i=0):
        print("%s%s" % (" " * i, self.metadata))
        for c in self.children:
            c.pprint(i+2)

################################################################################
# optimization stuff

def golden_section_minimization(a, b, f, done):
    gr = (5 ** 0.5 + 1) / 2
    fa = f(a)
    fb = f(b)
    # from wikipedia
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    fc = f(c)
    fd = f(d)
    while not done(c, d, fc, fd):
        if f(c) < f(d):
            b = d
        else:
            a = c
        # we recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    return (c + d) / 2

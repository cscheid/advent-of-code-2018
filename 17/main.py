# 10:35
#   14:50
#   14:52
import sys

f = sys.stdin.readlines()

def parse_line(l):
    l = l.strip().split(', ')
    left = l[0].split('=')
    right = l[1].split('=')
    right = right[1].split('..')
    if left[0] == 'x':
        return ((int(left[1]), int(right[0])),
                (int(left[1]), int(right[1])))
    else:
        return ((int(right[0]), int(left[1])),
                (int(right[1]), int(left[1])))

def left_of(p):
    return (p[0]-1, p[1])
def right_of(p):
    return (p[0]+1, p[1])
def left(p):
    return (p[0]-1, p[1])
def right(p):
    return (p[0]+1, p[1])
def under(p):
    return (p[0], p[1]+1)
def over(p):
    return (p[0], p[1]-1)
def below(p):
    return (p[0], p[1]+1)
def above(p):
    return (p[0], p[1]-1)

def find_bounds(lines):
    min_x = min(l[0][0] for l in lines)
    max_x = max(l[1][0] for l in lines)
    min_y = min(l[0][1] for l in lines)
    max_y = max(l[1][1] for l in lines)
    if min_x > 500:
        min_x = 500
    if max_x < 500:
        max_x = 500
    if min_y > 0:
        min_y = 0
    if max_y < 0:
        max_y = 0
    return ((min_x-1, min_y), (max_x+1, max_y))

total_water = 0
class Board:
    def __init__(self, lines):
        bounds = find_bounds(lines)
        ((min_x, min_y), (max_x, max_y)) = bounds
        print("bounds: ", ((min_x, min_y), (max_x, max_y)))
        self.bounds = bounds
        board = []
        for y in range(min_y, max_y+1):
            board.append(["."] * (max_x - min_x + 1))
        self.board = board
        for ((lmnx, lmny), (lmxx, lmxy)) in lines:
            lmnx -= min_x
            lmny -= min_y
            lmxx -= min_x
            lmxy -= min_y
            for y in range(lmny, lmxy + 1):
                for x in range(lmnx, lmxx + 1):
                    self.board[y][x] = '#'
        spring_location = (500 - min_x, 0 - min_y)
        self.spring_location = spring_location
        self.board[spring_location[1]][spring_location[0]] = '+'
    def pprint(self):
        for y in self.board:
            print("".join(y))
    def enumerate_squares(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                yield (x, y)
    def enumerate_range(self, min_point, max_point):
        for y in range(min_point[1], max_point[1]+1):
            for x in range(min_point[0], max_point[0]+1):
                yield x, y
    def find_water(self):
        for (x, y) in self.enumerate_squares():
            if self.board[y][x] in ['|', '~']:
                yield (x, y)
    def find_static_water(self):
        for (x, y) in self.enumerate_squares():
            if self.board[y][x] in ['~']:
                yield (x, y)
    def set_square_at(self, p, v):
        self.board[p[1]][p[0]] = v
    def square_at(self, p):
        try:
            return self.board[p[1]][p[0]]
        except IndexError:
            return None
    def raycast(self, origin, d, cond=lambda t: True):
        p = origin
        try:
            while cond(p):
                p = (p[0] + d[0], p[1] + d[1])
        except IndexError:
            return None
        return p
    
    def check_for_static_water(self, p):
        if self.square_at(p) == '#':
            r = self.raycast(right(p), (1, 0), lambda p: self.square_at(p) == '|' and self.square_at(below(p)) in ['~', '#'])
            if r and self.square_at(r) == '#':
                for x in range(p[0]+1, r[0]):
                    self.set_square_at((x, p[1]), '~')
                    self.open_squares.add((x, p[1]-1))
            l = self.raycast(left(p), (-1, 0), lambda p: self.square_at(p) == '|' and self.square_at(below(p)) in ['~', '#'])
            if l and self.square_at(l) == '#':
                for x in range(l[0]+1, p[0]):
                    self.set_square_at((x, p[1]), '~')
                    self.open_squares.add((x, p[1]-1))
        elif self.square_at(p) == '|' and self.square_at(below(p)) in ['~', '#', '|']:
            l = self.raycast(left(p), (-1, 0), lambda p: self.square_at(p) == '|' and self.square_at(below(p)) in ['~', '#'])
            r = self.raycast(right(p), (1, 0), lambda p: self.square_at(p) == '|' and self.square_at(below(p)) in ['~', '#'])
            if l and r and self.square_at(l) == '#' and self.square_at(r) == '#':
                for x in range(l[0]+1, r[0]):
                    self.set_square_at((x, p[1]), '~')
                    self.open_squares.add((x, p[1]-1))

    def handle_square(self, p):
        if self.square_at(p) == '.' and (self.square_at(above(p)) in ['|', '+']):
            self.set_square_at(p, '|')
            self.check_for_static_water(p)
            self.open_squares.add(below(p))
            self.open_squares.add(p)
            if self.square_at(left(p)) == '.' and self.square_at(below(p)) in ['~', '#'] and self.square_at(below(left(p))) in ['~', '#']:
                self.open_squares.add(left(p))
            if self.square_at(right(p)) == '.' and self.square_at(below(p)) in ['~', '#'] and self.square_at(below(right(p))) in ['~', '#']:
                self.open_squares.add(right(p))
        elif self.square_at(p) == '.' and (self.square_at(right(p)) == '|') and (self.square_at(below(p)) in ['~', '|', '#']):
            self.set_square_at(p, '|')
            self.check_for_static_water(p)
            self.open_squares.add(left(p))
            self.open_squares.add(below(p))
            self.open_squares.add(p)
        elif self.square_at(p) == '.' and (self.square_at(left(p)) == '|') and (self.square_at(below(p)) in ['~', '|', '#']):
            self.set_square_at(p, '|')
            self.check_for_static_water(p)
            self.open_squares.add(right(p))
            self.open_squares.add(below(p))
            self.open_squares.add(p)
        elif self.square_at(p) == '#':
            self.check_for_static_water(p)
        elif self.square_at(p) == '|':
            self.open_squares.add(below(p))
            self.check_for_static_water(p)
            if self.square_at(left(p)) == '.' and self.square_at(below(p)) in ['~', '#']:
                self.set_square_at(left(p), '|')
                self.open_squares.add(left(p))
                self.open_squares.add(below(left(p)))
                self.check_for_static_water(left(p))
            if self.square_at(right(p)) == '.' and self.square_at(below(p)) in ['~', '#']:
                self.set_square_at(right(p), '|')
                self.open_squares.add(right(p))
                self.open_squares.add(below(right(p)))
                self.check_for_static_water(right(p))
            
    def run(self):
        self.open_squares = set()
        self.open_squares.add(below(self.spring_location))
        while len(self.open_squares):
            self.handle_square(self.open_squares.pop())
        
lines = list(parse_line(l) for l in f)
board = Board(lines)
d = 0
board.run()
board.pprint()
print("The first count is slightly wrong because my bounds include things out of the scan; I just subtracted the appropriate number of '|' tiles manually")
print(len(list(i for i in board.find_water())))
print(len(list(i for i in board.find_static_water())))


# start: 8:46AM
#   part1: 9:36AM
#   part2: 9:42AM

import sys

def parse_loop_from_senw(x, y, ls):
    # is this a valid loop?
    try:
        east = ls[y][x+1]
        south = ls[y+1][x]
        if (south != '|' and south != 'v' and south != '^' and south != '+') and \
           (east != '-' and east != '<' and east != '>' and east != '+'):
            return None
        # ok, this is a loop starting from that corner
        # find east coordinates
        cx = x+1
        while ls[y][cx] != '\\':
            cx = cx + 1
        cy = y+1
        while ls[cy][x] != '\\':
            cy = cy + 1
        return (x, y, cx, cy)
    except IndexError:
        return None

def locate_loop(x, y, c):
    global loops
    for i, loop in enumerate(loops):
        left, top, right, bottom = loop
        if (c == '^' or c == 'v') and (x == left or x == right) and y >= top and y <= bottom:
            return i # [x, y, c, i]
        if (c == '<' or c == '>') and (y == top or y == bottom) and x >= left and x <= right:
            return i # [x, y, c, i]
    raise Exception("Could not locate loop for cart %s at %s,%s" % (c, x, y))

turn_right = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
turn_left = {'>': '^', '^': '<', '<': 'v', 'v': '>'}

class Cart:
    def __repr__(self):
        global loops
        return "x:%s y:%s, c:%s, loop:%s" % (self.x, self.y, self.c, loops[self.loop])
    def __init__(self, x, y, c, loop):
        self.turns = 0
        self.x = x
        self.y = y
        self.c = c
        self.loop = loop
    def turn(self):
        global loops
        which = self.turns % 3
        if which == 0:
            self.c = turn_left[self.c]
        elif which == 1:
            pass
        elif which == 2:
            self.c = turn_right[self.c]
        self.turns += 1
        self.loop = locate_loop(self.x, self.y, self.c)
    def move(self):
        global loops
        left, top, right, bottom = loops[self.loop]
        c = self.c
        if c == '^':
            if self.y > top:
                self.y -= 1
            else:
                if self.x == left:
                    self.c = '>'
                    self.x += 1
                else:
                    self.c = '<'
                    self.x -= 1
        elif c == '<':
            if self.x > left:
                self.x -= 1
            else:
                if self.y == bottom:
                    self.c = '^'
                    self.y -= 1
                else:
                    self.c = 'v'
                    self.y += 1
        elif c == 'v':
            if self.y < bottom:
                self.y += 1
            else:
                if self.x == left:
                    self.c = '>'
                    self.x += 1
                else:
                    self.c = '<'
                    self.x -= 1
        elif c == '>':
            if self.x < right:
                self.x += 1
            else:
                if self.y == bottom:
                    self.c = '^'
                    self.y -= 1
                else:
                    self.c = 'v'
                    self.y += 1
        else:
            raise Exception("unexpected cart %s" % c)
    def step(self):
        self.move()
        if board[self.y][self.x] == '+':
            self.turn()

def print_board():
    board_list = list(list(c for c in l) for l in board)
    for c in carts:
        board_list[c.y][c.x] = c.c
    for l in board_list:
        print("".join(l).strip('\n'))
    print()
    
def read_board():
    global board
    global loops
    global carts
    for i, l in enumerate(board):
        for j, c in enumerate(l):
            if c == '/':
                r = parse_loop_from_senw(j, i, board)
                if r:
                    loops.append(r)
            
    for i, l in enumerate(board):
        for j, c in enumerate(l):
            if c in ['^', 'v', '<', '>']:
                # dangerous..
                board_line = list(c for c in l)
                board_line[j] = '-' if c in ['<', '>'] else '|'
                board[i] = "".join(board_line)
                carts.append(Cart(j, i, c, locate_loop(j, i, c)))

def remove_collisions(x, y):
    global carts
    carts = list(c for c in carts if c.x != x or c.y != y)
    return check_collisions()

def check_collisions():
    s = set()
    for v in carts:
        k = (v.x, v.y)
        if k in s:
            print("crash %s %s" % (v.x, v.y))
            return remove_collisions(v.x, v.y)
        else:
            s.add(k)
    return len(carts)

def tick():
    carts.sort(key=lambda cart: (cart.y, cart.x))
    for cart in carts:
        cart.step()
        c = check_collisions()
    return len(carts) <= 1

board = sys.stdin.readlines()
carts = []
loops = []
read_board()
# print(board)
# print(loops)
# print(carts)

ticks = 0
# print_board()
while not tick():
    ticks += 1
#     print_board()
    # print(ticks, carts)
if len(carts) >= 1:
    print("%s,%s" % (carts[0].x, carts[0].y))
print(ticks)

# 10:35AM

import sys
import time

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
def under(p):
    return (p[0], p[1]+1)
def over(p):
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
        # x sentinels
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
    def square_at(self, p):
        return self.board[p[1]][p[0]]
    def raycast(self, origin, d, cond=lambda t: True):
        p = origin
        try:
            while self.square_at(p) == '.' and cond(p):
                p = (p[0] + d[0], p[1] + d[1])
        except IndexError:
            return None
        return p
    def pour_from(self, p, indent=0):
        global total_water
        # print(" " * indent, "will pour from", p)
        # raycast from spring to first clay or pooled water
        p = under(p)
        p = self.raycast(p, (0, 1))
        if p is None:
            # print("miss! at ", p)
            return False
        # print("hit! %s at %s" % (self.square_at(p), p))
        water_hit = (p[0], p[1]-1)
        if self.square_at(water_hit) != '.':
            return False
        left_boundary = self.raycast(water_hit, (-1, 0))
        if left_boundary is None:
            left_boundary = (0, water_hit[1])
        right_boundary = self.raycast(water_hit, (1, 0))
        if right_boundary is None:
            right_boundary = (self.bounds[1][0], water_hit[1])
        if all(self.square_at(under(ray_p)) in ['#', '~']
               for ray_p in self.enumerate_range(right_of(left_boundary), left_of(right_boundary))):
            # print("will fill at %s %s %s" % (water_hit, left_boundary[0]+1, right_boundary[0]))
            for x in range(left_boundary[0]+1, right_boundary[0]):
                self.board[left_boundary[1]][x] = '~'
                total_water += 1 
            return True
        else:
            result = False
            # print("Can't fill, will pour from leaks")
            p = self.raycast(water_hit, (-1, 0), lambda p: self.square_at(under(p)) in ['#', '~'])
            if not (p is None) and self.square_at(p) == '.':
                result = result or self.pour_from(p, indent+2)
            p = self.raycast(water_hit, (1, 0), lambda p: self.square_at(under(p)) in ['#', '~'])
            if not (p is None) and self.square_at(p) == '.':
                result = result or self.pour_from(p, indent+2)
            return result
    def tick(self):
        return self.pour_from(self.spring_location)
            
        
lines = list(parse_line(l) for l in f)
board = Board(lines)
print(board.bounds)
exit(1)
# board.pprint()
d = 0
while board.tick():
    print(d, total_water)
    d += 1
    # board.pprint()
    pass
    # time.sleep(1)
    
print(len(list(i for i in board.find_water())))
# for l in lines:
#     print(l)
# print(find_bounds(lines))


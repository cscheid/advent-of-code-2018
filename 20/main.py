#!/usr/bin/env pypy3
# 8:26AM
#  9:44AM
#  9:53AM

from kitchen_sink import *

import sys
l = sys.stdin.readline().strip()

def parse_it():
    i = 1

    def parse_straight_path():
        nonlocal i
        p = []
        p.append(l[i])
        i += 1
        while l[i] in 'NSWE':
            p.append(l[i])
            i += 1
        return ("straight", "".join(p))

    def parse_branch():
        nonlocal i
        branches = []
        current_branch = []
        assert(l[i] == '(')
        i += 1
        while True:
            v = l[i]
            if v in 'NSWE':
                current_branch.append(parse_straight_path())
            elif v == '(':
                current_branch.append(parse_branch())
            elif v == '|':
                i += 1
                branches.append(("sequence", current_branch))
                current_branch = []
            elif v == ')':
                i += 1
                branches.append(("sequence", current_branch))
                return ("option", branches)
            else:
                raise Exception("Expected NSWE(|) at %s" % v)
        
    def parse_input():
        nonlocal i
        current_parse = []
        while True:
            v = l[i]
            if v in 'NSWE':
                current_parse.append(parse_straight_path())
            elif v == '(':
                current_parse.append(parse_branch())
            elif v == '$':
                return ("sequence",current_parse)
            else:
                raise Exception("expected NSWE($ at %s" % v)

    return parse_input()

infinity = 10000000

markings = []
def walk(direction, position):
    dx = {'N': 0,  'S': 0,  'E': 1, 'W': -1}
    dy = {'N': -1, 'S': +1, 'E': 0, 'W': 0}
    markings.append((position[0] * 2 + dx[direction], position[1] * 2 + dy[direction], '.'))
    return (position[0] + dx[direction], position[1] + dy[direction])

min_px = infinity
min_py = infinity
def update(position):
    global min_px
    global min_py
    min_px = min(min_px, position[0])
    min_py = min(min_py, position[1])
    markings.append((position[0] * 2, position[1] * 2, '.'))

def interpret_straight(command, positions):
    result = set()
    for position in positions:
        this_position = position
        update(this_position)
        for direction in command[1]:
            this_position = walk(direction, this_position)
            update(this_position)
        result.add(this_position)
    return result

def interpret_sequence(command, positions):
    result = set()
    for position in positions:
        this_positions = set([position])
        for subcommand in command[1]:
            this_positions = interpret(subcommand, this_positions)
        result.update(this_positions)
    return result

def interpret_option(command, positions):
    result = set()
    for position in positions:
        this_positions = set([position])
        for option in command[1]:
            result.update(interpret(option, this_positions))
    return result

def interpret(command, positions):
    if command[0] == 'straight': return interpret_straight(command, positions)
    if command[0] == 'option':   return interpret_option(command, positions)
    if command[0] == 'sequence': return interpret_sequence(command, positions)
    else:
        raise Exception("Unknown command")

interpret(parse_it(), set([(0,0)]))

min_x = min(m[0] for m in markings)
max_x = max(m[0] for m in markings)
min_y = min(m[1] for m in markings)
max_y = max(m[1] for m in markings)

b = Board.constant(max_x - min_x + 1, max_y - min_y + 1, "#")
for m in markings:
    b[m[1] - min_y][m[0] - min_x] = '.'
b = b.sentinel('#')
b.pprint_char()

mv = -infinity
c = 0
def ignore_doors(x, y, c):
    if x % 2 == 0:
        return infinity
    if y % 2 == 0:
        return infinity
    return c
ds = b.shortest_path_from(2 * (-min_px) + 1, 2 * (-min_py) + 1, lambda s: s == '.', infinity=infinity)
ds = ds.map(lambda x, y, c: c if c == infinity else int(c/2))
ds = ds.map(ignore_doors)

c = isize(filter(lambda v: v != infinity and v >= 1000, ds.values()))
mv = max(filter(lambda v: v != infinity, ds.values()))

print(mv, c)
        

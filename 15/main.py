#!/usr/bin/env python3

# 8:59AM
#   11:13AM
#   11:42AM

from kitchen_sink import *
import sys
import time

elves_power = int(sys.argv[1])
infinity = 1000000

class ElvesBoard:
    def __init__(self):
        self.starting_board = Board(input_lines())
        self.identify_units()
        self.rounds = 0
        self.populate_this_turn()
    def populate_this_turn(self):
        result = self.clean_board.clone()
        for unit in self.units:
            result[unit[1]][unit[0]] = unit[3]
        self.current_board = result
    def identify_units(self):
        b = self.starting_board
        units = []
        for x, y, c in b.items():
            if c in ['E', 'G']:
                units.append([x, y, 200, c])
        self.clean_board = b.map(lambda x, y, v: v.replace('E', '.').replace('G', '.'))
        units.sort(key=lambda x:(x[1],x[0]))
        self.units = units
    def step(self):
        self.populate_this_turn()
        print("After %d rounds" % self.rounds)
        self.pprint()
        # time.sleep(5)
        for i, unit in enumerate(self.units):
            if unit[2] <= 0:
                # unit is dead
                continue
            print("unit will move.", unit)
            goblins_live = len(list(u for u in self.units if u[3] == 'G' and u[2] > 0)) > 0
            elves_live = len(list(u for u in self.units if u[3] == 'E' and u[2] > 0)) > 0
            if not goblins_live or not elves_live:
                self.units = sorted(list(u for u in self.units if u[2] > 0),
                                    key = lambda x: (x[1], x[0]))
                return False
            # print("Step for unit", unit)
            t = self.find_targets(unit)
            # print("targets: ", t)
            if t is None:
                # print("moving")
                unit_distance_map = self.shortest_path_from(unit[0], unit[1])
                # self.print_d(unit_distance_map)
                self.move(unit, unit_distance_map)
                t = self.find_targets(unit)
                # print("new targets:", t)
            if t:
                # print("will attack")
                self.attack(unit, t)
            # print("after move:", unit)
            self.pprint()
            # time.sleep(5)

        # unit cleanup and move priority reorder
        self.units = sorted(list(u for u in self.units if u[2] > 0),
                            key = lambda x: (x[1], x[0]))
        self.rounds += 1
        return True
    def find_targets(self, unit):
        potential_targets = []
        for nx, ny in self.neighbor_squares(unit[0], unit[1]):
            if (self.current_board[ny][nx] in ['G', 'E']) and (unit[3] != self.current_board[ny][nx]):
                for potential_target in self.units:
                    if potential_target[2] <= 0:
                        continue
                    if potential_target[0] == nx and potential_target[1] == ny:
                        potential_targets.append(potential_target)
                        break
        potential_targets.sort(key = lambda unit: (unit[2], unit[1], unit[0]))
        if len(potential_targets) == 0:
            return None
        else:
            return potential_targets[0]
    def neighbor_squares(self, x, y):
        return [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
    def move(self, unit, distance_map):
        def open_target_squares():
            result = set()
            for u in self.units:
                if u[3] == unit[3]:
                    continue
                if u[2] <= 0:
                    # dead unit not cleaned up yet
                    continue
                for nx, ny in self.neighbor_squares(u[0], u[1]):
                    if self.current_board[ny][nx] == '.' and distance_map[ny][nx] != infinity:
                        result.add((nx, ny))
            return sorted(list(v for v in result), key=lambda v: (distance_map[v[1]][v[0]], v[1], v[0]))
        s = open_target_squares()
        if len(s) == 0:
            return
        where = s[0]
        dft = self.shortest_path_from(where[0], where[1])
        direction = list((dx, dy) for dx, dy in self.neighbor_squares(unit[0], unit[1])
                         if self.current_board[dy][dx] == '.')
        direction.sort(key = lambda k: (dft[k[1]][k[0]], k[1], k[0]))
        if len(direction) == 0:
            return
        where = direction[0]
        self.current_board[unit[1]][unit[0]] = '.'
        self.current_board[where[1]][where[0]] = unit[3]
        unit[0] = where[0]
        unit[1] = where[1]
    def attack(self, unit, target):
        if unit[3] == 'G':
            target[2] -= 3
        else:
            target[2] -= elves_power
        if target[2] <= 0:
            # clean up current board
            self.current_board[target[1]][target[0]] = '.'
    def shortest_path_from(self, x, y):
        return self.current_board.shortest_path_from(x, y, lambda s: s == '.', infinity=infinity)
    def print_d(self, d):
        print("distance: ")
        for l in d:
            for v in l:
                print("%s\t" % v, end='')
            print()
        
    def pprint(self):
        print(self.units)
        self.current_board.pprint_char()
        print(self.outcome())

    def outcome(self):
        th = 0
        for u in self.units:
            th += u[2]
        print(th, self.rounds)
        return self.rounds * th
    def populations(self):
        print("Elves: %d" % len(list(l for l in self.units if l[3] == 'E')))
        print("Goblins: %d" % len(list(l for l in self.units if l[3] == 'G')))
b = ElvesBoard()
b.populations()
# b.pprint()
while b.step():
    pass
    # b.pprint()
b.pprint()
b.populations()
print(b.outcome())
# b.step()

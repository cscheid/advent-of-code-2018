#!/usr/bin/env python3

n_players, last_marble = 438, 7162600
scores = [0] * n_players

class Node:
    def __init__(self, v):
        self.next = self
        self.prev = self
        self.v = v
    def remove_self(self):
        t = self.next
        self.next.prev = self.prev
        self.prev.next = self.next
    def pprint(self):
        s = self
        c = self
        print("%02d %s (prev: %s) (next: %s)" % (c.v, c, c.prev, c.next))
        c = c.next
        while c != s:
            print("%02d %s (prev: %s) (next: %s)" % (c.v, c, c.prev, c.next))
            c = c.next
    def add(self, v):
        new = Node(v)
        new.next = self.next
        new.prev = self
        self.next.prev = new
        self.next = new
        return new

def init():
    return (Node(0), 1, 1)

current_state = init()
        
def step(state):
    circle, next_marble, player = state
    if next_marble % 23 == 0:
        to_remove = circle.prev.prev.prev.prev.prev.prev.prev
        scores[player] += next_marble
        scores[player] += to_remove.v
        circle = to_remove.next
        to_remove.remove_self()
    else:
        circle = circle.next
        circle.add(next_marble)
        circle = circle.next
    return circle, next_marble + 1, (player + 1) % n_players

current_state = init()
current_state[0].pprint()
while current_state[1] < last_marble:
    current_state = step(current_state)
    if current_state[1] % 1000 == 0:
        print("\r                        \r%s" % current_state[1], end='')

print()
print(max(scores))


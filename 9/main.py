#!/usr/bin/env pypy3

from kitchen_sink import *

n_players, last_marble = 438, 7162600
scores = [0] * n_players

def init():
    result = deque()
    result.extend([0])
    return (result, 1, 1)

current_state = init()
        
def step(state):
    circle, next_marble, player = state
    if next_marble % 23 == 0:
        circle.rotate(7)
        v = deque_top(circle)
        scores[player] += next_marble
        scores[player] += v
        circle.popleft()
    else:
        circle.rotate(-2)
        circle.appendleft(next_marble)
    return circle, next_marble + 1, (player + 1) % n_players

current_state = init()
print(current_state)
while current_state[1] < last_marble:
    current_state = step(current_state)
    if current_state[1] % 1000 == 0:
        print("\r                        \r%s" % current_state[1], end='')

print()
print(max(scores))


#!/usr/bin/env pypy3
from kitchen_sink import *

def count(ws):
    v2 = 0
    v3 = 0
    for w in ws:
        h = group_by_count(w)
        if len(h.get(2, [])) > 0:
            v2 += 1
        if len(h.get(3, [])) > 0:
            v3 += 1
    return v2 * v3

def diff(ws):
    for w1 in ws:
        for w2 in ws:
            diff = sum(1 if l1 != l2 else 0 for l1, l2 in zip(w1, w2))
            if diff == 1:
                common = "".join(l1 for l1, l2 in zip(w1, w2) if l1 == l2)
                return common

ws = input_lines()
print("part 1:", count(ws))
print("part 2:", diff(ws))

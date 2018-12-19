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

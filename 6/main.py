#!/usr/bin/env pypy3
from kitchen_sink import *

import sys

def read_points(ls):
    result = []
    for l in ls:
        l = l.split(', ')
        result.append((int(l[0]), int(l[1])))
    return result

def center(points, bound):
    return list((p[0] - bound[0][0] + 1, p[1] - bound[1][0] + 1) for p in points)

def find_bounds(l):
    min_x = min(a[0] for a in l)
    min_y = min(a[1] for a in l)
    max_x = max(a[0] for a in l)
    max_y = max(a[1] for a in l)
    return (min_x, max_x), (min_y, max_y)
infinity = 1000000

def l1_distance_board(w, h, point):
    return map_board(lambda p: abs(point[0] - p[0]) + abs(point[1] - p[1]),
                     index_board(w, h))

def update_board(distances, index, argclosest, closest):
    w, h = dims_board(distances)
    for x, y in enumerate_board(distances):
        if distances[y][x] < closest[y][x]:
            argclosest[y][x] = index
            closest[y][x] = distances[y][x]

def count_regions(distances, indices, points):
    d = {}
    weights = sentinel_board(map_board(const(1), indices), infinity)
    for x, y in enumerate_board(indices):
        i = indices[y][x]
        count = 0
        for p in points:
            dist = abs(p[0] - x) + abs(p[1] - y)
            if dist == distances[y][x]:
                count += 1
        if count == 1:
            d[i] = d.get(i, 0) + weights[y][x]
    result = list((chr(k + 65), v) for (k, v) in d.items()
                  if v < infinity)
    result.sort(key=lambda v:-v[1])
    return result

# 6.1
if __name__ == '__main__':
    if sys.argv[1] == '1':
        l = read_points(input_lines())
        bounds = find_bounds(l)
        w = bounds[0][1] - bounds[0][0] + 2
        h = bounds[1][1] - bounds[1][0] + 2
        l = center(l, bounds)
        argclosest_board = constant_board(w, h, -1)
        closest_board = constant_board(w, h, infinity)
        for i, p in enumerate(l):
            update_board(l1_distance_board(w, h, p),
                         i,
                         argclosest_board,
                         closest_board)
        print(count_regions(closest_board, argclosest_board, l))
    elif sys.argv[1] == '2':
        l = read_points(input_lines())
        bounds = find_bounds(l)
        w = bounds[0][1] - bounds[0][0] + 2
        h = bounds[1][1] - bounds[1][0] + 2
        l = center(l, bounds)
        total = empty_board(w, h)
        for i, p in enumerate(l):
            d = l1_distance_board(w, h, p)
            total = add_board(d, total)
        count = 0
        for x in range(w):
            for y in range(h):
                if total[y][x] < 10000:
                    count += 1
        print(count)
    

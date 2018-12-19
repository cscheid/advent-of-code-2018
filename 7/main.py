#!/usr/bin/env pypy3

from kitchen_sink import *
import sys

def parse_input(ls):
    result = []
    for l in ls:
        l = l.split()
        result.append((l[1], l[7]))
    return Graph(result)

def part1(g):
    return "",join(g.topo_sort())

def topo_sort_2(g):
    sources = list(g.sources())
    sources.sort(key=lambda k: -ord(k))
    result = []
    n_workers = 5
    current_second = 0
    available_workers = 5
    worker_queue = []
    working_set = set()
    not_done_set = set(g.vertices())
    while len(sources) or len(worker_queue):
        for w in worker_queue:
            if w[1] == 0:
                available_workers += 1
                f = w[0]
                working_set.remove(f)
                not_done_set.remove(f)
                if f in g:
                    g.remove(f)
                sources = list(v for v in sources if v != f)
                sources.extend(list(k for k in g.vertices() if g.in_degree(k) == 0 and k not in working_set))
                sources.sort(key=lambda k: -ord(k))
                result.append(f)
        worker_queue = list(w for w in worker_queue if w[1] != 0)
        while available_workers > 0 and len(sources):
            available_workers -= 1
            f = sources.pop()
            sources = list(v for v in sources if v != f)
            working_set.add(f)
            worker_queue.append([f, 60 + ord(f) - 64])
        if available_workers == 0 or len(sources) == 0 and len(not_done_set) > 0:
            current_second += 1
            for i in range(len(worker_queue)):
                worker_queue[i][1] -= 1
            continue
    print("".join(result), current_second)

if __name__ == '__main__':
    g = parse_input(input_lines())
    # print(part_1(g))
    topo_sort_2(g)

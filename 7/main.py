import sys

def parse_input(ls):
    result = []
    for l in ls:
        l = l.split()
        result.append((l[1], l[7]))
    d = {}
    d_inv = {}
    v_set = set()
    for (f, t) in result:
        d.setdefault(f, []).append(t)
        d_inv.setdefault(t, []).append(f)
        v_set.add(f)
        v_set.add(t)
    for v in v_set:
        d.setdefault(v, [])
    return d, d_inv

def in_degree(d, d_inv, k):
    return len(d_inv.get(k, []))

def topo_sort(d, d_inv):
    sources = list(k for k in d.keys() if in_degree(d, d_inv, k) == 0)
    print(sources)
    sources.sort(key=lambda k: -ord(k))
    result = []
    while len(sources):
        f = sources.pop()
        sources = list(v for v in sources if v != f)
        if f in d:
            for t in d[f]:
                d_inv[t].remove(f)
            del d[f]
        result.append(f)
        sources.extend(list(k for k in d.keys() if in_degree(d, d_inv, k) == 0))
        sources.sort(key=lambda k: -ord(k))
    print("".join(result))

def topo_sort_2(d, d_inv):
    sources = list(k for k in d.keys() if in_degree(d, d_inv, k) == 0)
    print(sources)
    sources.sort(key=lambda k: -ord(k))
    result = []
    n_workers = 5
    current_second = 0
    available_workers = 5
    worker_queue = []
    working_set = set()
    not_done_set = set(k for k in d.keys())
    while len(sources) or len(worker_queue):
        for w in worker_queue:
            if w[1] == 0:
                available_workers += 1
                f = w[0]
                working_set.remove(f)
                not_done_set.remove(f)
                if f in d:
                    for t in d[f]:
                        d_inv[t].remove(f)
                    del d[f]
                sources = list(v for v in sources if v != f)
                sources.extend(list(k for k in d.keys() if in_degree(d, d_inv, k) == 0 and k not in working_set))
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
    d, d_inv = parse_input(sys.stdin.readlines())
    # topo_sort(d, d_inv)
    topo_sort_2(d, d_inv)

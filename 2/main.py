def histogram(w):
    result = {}
    for l in w:
        result[l] = result.get(l, 0) + 1
    inv = {}
    for (k, v) in result.items():
        inv.setdefault(v, []).append(k)
    return inv

def count(ws):
    v2 = 0
    v3 = 0
    for w in ws:
        h = histogram(w)
        if len(h.get(2, [])) > 0:
            v2 += 1
        if len(h.get(3, [])) > 0:
            v3 += 1
    return v2 * v3

def histogram2(w):
    result = {}
    for l in w:
        result[l] = result.get(l, 0) + 1
    return result

def diff(ws):
    for w1 in ws:
        for w2 in ws:
            diff = sum(1 if l1 != l2 else 0 for l1, l2 in zip(w1, w2))
            if diff == 1:
                print("Words:")
                print(w1)
                print(w2)
                common = "".join(l1 for l1, l2 in zip(w1, w2) if l1 == l2)
                print("Common: ", common)
                break

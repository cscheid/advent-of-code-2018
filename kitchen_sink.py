def permutations(lst):
    if len(lst) == 0:
        yield []
    for i in range(len(lst)):
        rest = lst[:i] + lst[i+1:]
        for p in permutations(rest):
            yield [lst[i]] + p

def pairs(lst):
    return zip(lst, lst[1:])

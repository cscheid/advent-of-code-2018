#!/usr/bin/env pypy3

from kitchen_sink import *

import sys

class MyTree(Tree):

    def __init__(self, *args):
        Tree.__init__(self, *args)

    def metadata_sum(self):
        this_sum = sum(self.metadata)
        other_sum = sum(c.metadata_sum() for c in self.children)
        return this_sum + other_sum

    def value(self):
        if len(self.children) == 0:
            return self.metadata_sum()
        else:
            s = 0
            for v in self.metadata:
                try:
                    s += self.children[v-1].value()
                except IndexError:
                    pass
            return s
    
def parse_input(vs):
    children = []
    metadata = []
    n_children = next(vs)
    n_metadata = next(vs)
    for i in range(n_children):
        children.append(parse_input(vs))
    for i in range(n_metadata):
        metadata.append(next(vs))
    return MyTree(children, metadata)

if __name__ == '__main__':
    vs = (int(i) for i in input_lines()[0].split())
    tree = parse_input(vs)
    print(tree.metadata_sum())
    print(tree.value())

    

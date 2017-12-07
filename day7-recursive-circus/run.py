#!/usr/bin/env python3

import statistics

from collections import defaultdict, deque


class Program:

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.parents = {}
        self.children = {}

    def __str__(self):
        return "{}[{}]".format(
            self.name, ' '.join(sorted(self.parents)))


def build_tree(data):
    data = data.strip().split('\n')
    data.sort(key=lambda entry: '->' in entry)
    data = deque(data)

    elems = dict()

    while len(data):
        entry = data.popleft()

        if '->' in entry:
            name, weight, _, *parents = entry.split()
            parents = [e.strip(',') for e in parents]
        else:
            name, weight = entry.split()
            parents = []

        weight = int(weight.strip('()'))

        if name not in elems:
            elems[name] = Program(name, weight)

        try:
            for parent in parents:
                elems[name].parents[parent] = elems[parent]
                elems[parent].children[name] = elems[name]
                assert all(type(parent) == Program
                    for parent in elems[name].parents.values())
                assert all(type(child) == Program
                    for child in elems[parent].children.values())
        except KeyError:
            data.append(entry)

    return elems


def depth(prog):
    if not prog.parents.values():
        return 0
    else:
        return max(depth(p) for p in prog.parents.values()) + 1


def puzzle(tree):
    return max(tree.values(), key=depth)


def height(prog):
    return prog.weight + sum(height(p) for p in prog.parents.values())


def is_balanced(prog):
    if not prog.parents.values():
        return True
    else:
        heights = [height(p) for p in prog.parents.values()]
        if max(heights) != min(heights):
            return False
        else:
            return True


def find_unbalanced_parent(prog):
    parents = prog.parents.values()
    heights = [height(e) for e in parents]
    mode = statistics.mode(heights)
    unbal = next((p for p, h in zip(parents, heights) if h != mode), None)

    if unbal:
        return unbal, mode - height(unbal)
    else:
        return None, 0


def puzzle2(tree):
    disc = [e for e in tree.values() if not is_balanced(e)]
    parent, delta = find_unbalanced_parent(disc[0])
    return parent.weight + delta


inp = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

elems = build_tree(inp)
assert elems

# test parents
assert sorted(elems['tknk'].parents.keys()) == sorted(['ugml', 'padx', 'fwft'])
assert sorted(elems['ugml'].parents.keys()) == sorted(['gyxo', 'ebii', 'jptl'])
assert sorted(elems['fwft'].parents.keys()) == sorted(['ktlj', 'cntj', 'xhth'])

# test children
assert list(elems['ugml'].children.keys()) == ['tknk']
assert list(elems['padx'].children.keys()) == ['tknk']
assert list(elems['fwft'].children.keys()) == ['tknk']
assert list(elems['ebii'].children.keys()) == ['ugml']

# depths
assert all(depth(elems[e]) == 0 for e in ['gyxo', 'havc', 'xhth'])
assert all(depth(elems[e]) == 1 for e in ['ugml', 'padx', 'fwft'])
assert depth(elems['tknk']) == 2

# heights
assert height(elems['ktlj']) == 57
assert height(elems['cntj']) == 57
assert height(elems['xhth']) == 57
assert height(elems['fwft']) == \
    72 + sum(height(elems[e]) for e in ['ktlj', 'cntj', 'xhth'])
assert height(elems['tknk']) == \
    41 + sum(height(elems[e]) for e in ['ugml', 'padx', 'fwft'])

# balancing
assert all(is_balanced(elems[e]) for e in ['gyxo', 'havc', 'xhth'])
assert all(is_balanced(elems[e]) for e in ['ugml', 'padx', 'fwft'])
assert not is_balanced(elems['tknk'])

assert puzzle(elems) == elems['tknk']

assert find_unbalanced_parent(elems['tknk']) == (elems['ugml'], -8)
assert puzzle2(elems) == 60


if __name__ == '__main__':
    with open('input') as f:
        tree = build_tree(f.read())
        print(puzzle(tree))
        print(puzzle2(tree))

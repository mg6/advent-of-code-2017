#!/usr/bin/env python3

from functools import reduce
from itertools import count


def redistribute(banks):
    num_banks = len(banks)
    at, val = reduce(lambda a, b: b if a[1] < b[1] else a, enumerate(banks)) 
    banks[at] = 0

    for i in range(val):
        banks[(at + 1 + i) % num_banks] += 1

    return banks


def redistribute_generator(banks):
    while True:
        banks = redistribute(banks)
        yield banks


def locate_redistribute_loop(banks):
    seen = dict()
    banks = redistribute_generator(banks)

    for step in count():
        bank = tuple(next(banks))
        if bank in seen:
            return (step, seen[bank])
        else:
            seen[bank] = step


def assert_next(iter, expected):
    actual = next(iter)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


banks = redistribute_generator([0, 2, 7, 0])
assert_next(banks, [2, 4, 1, 2])
assert_next(banks, [3, 1, 2, 3])
assert_next(banks, [0, 2, 3, 4])
assert_next(banks, [1, 3, 4, 1])
assert_next(banks, [2, 4, 1, 2])

pos, run_length = locate_redistribute_loop([0, 2, 7, 0])
assert pos + 1 == 5     # positions are 0-based!
assert (pos - run_length) == 4


if __name__ == '__main__':
    with open('input') as f:
        banks = [int(n) for n in f.read().strip().split()]
        pos, run_length = locate_redistribute_loop(banks)
        print(pos - run_length)

#!/usr/bin/env python3


from collections import defaultdict
from itertools import count


def array_from_sparse_dict(d):
    d = defaultdict(int, d)
    if not d:
        return []
    else:
        return [d[n] for n in range(0, 1 + max(d.keys()))]


assert array_from_sparse_dict({}) == []
assert array_from_sparse_dict({0: 3}) == [3]
assert array_from_sparse_dict({0: 3, 1: 2}) == [3, 2]
assert array_from_sparse_dict({0: 3, 2: 8}) == [3, 0, 8]
assert array_from_sparse_dict({1: 5, 2: 8}) == [0, 5, 8]


def scanner(depth, delay):
    offset = delay % (2 * (depth - 1))
    return 2 * (depth - 1) - offset if offset > depth - 1 else offset


def trip_severity(depths, delay=0):
    scanners = [scanner(depth, i + delay) for i, depth in enumerate(depths)]
    return sum(i * depth for i, depth in enumerate(depths) if scanners[i] == 0)


actual = trip_severity([3, 2, 0, 0, 4, 0, 4])
assert actual == 24, actual

actual = trip_severity([3, 2, 0, 0, 4, 0, 4], delay=4)
assert actual == 0, actual

actual = trip_severity([3, 2, 0, 0, 4, 0, 4], delay=10)
assert actual == 0, actual


def safe_trip(depths):
    for n in count():
        if all(scanner(depth, n + i) != 0 for i, depth in enumerate(depths)):
            return n


actual = safe_trip([3, 2, 0, 0, 4, 0, 4])
assert actual == 10, actual


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()

    lines = s.split('\n')
    depths = [list(map(int, line.split(': '))) for line in lines]
    depths = {e[0]: e[1] for e in depths}
    depths = array_from_sparse_dict(depths)
    print(trip_severity(depths))
    print(safe_trip(depths))

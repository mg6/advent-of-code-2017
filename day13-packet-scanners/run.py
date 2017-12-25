#!/usr/bin/env python3


from collections import defaultdict


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


# def scanner(layer, depth, delay=0):
#     return (layer + delay) % ((depth - 1) * 2) if (layer + delay) > depth else 0
#
#
# assert scanner(0, 3, delay=0) == 0
# assert scanner(0, 3, delay=1) == 1
# assert scanner(0, 3, delay=2) == 2
# assert scanner(0, 3, delay=3) == 1
# assert scanner(0, 3, delay=4) == 0
#
# assert scanner(2, delay=0) == 0, scanner(2, delay=0)
# assert scanner(2, delay=1) == 1, scanner(2, delay=1)
# assert scanner(2, delay=2) == 0, scanner(2, delay=2)
#
# assert scanner(1, delay=0) == 0, scanner(1, delay=0)
# assert scanner(1, delay=1) == 0, scanner(1, delay=1)


def scanner(depth):
    """
    Generates scanner positions for given depth.
    """
    if depth > 1:
        while True:
            for i in range(depth-1):
                yield i
            for i in range(depth-1, 0, -1):
                yield i
    elif depth == 1:
        while True:
            yield 0
    else:
        while True:
            yield None


sc = scanner(3)
assert next(sc) == 0
assert next(sc) == 1
assert next(sc) == 2
assert next(sc) == 1
assert next(sc) == 0
assert next(sc) == 1

sc = scanner(1)
assert next(sc) == 0
assert next(sc) == 0

sc = scanner(0)
assert next(sc) is None
assert next(sc) is None


def trip_severity(depths, delay=0):
    severity = None
    scanners = [scanner(n) for n in depths]

    for _ in range(delay):
        for s in scanners:
            next(s)

    for layer, depth in enumerate(depths):
        positions = [next(s) for s in scanners]
        if positions[layer] == 0:
            if severity is None:
                severity = 0
            severity += layer * depth

    return severity


assert trip_severity([3, 2, 0, 0, 4, 0, 4]) == 24
assert trip_severity([3, 2, 0, 0, 4, 0, 4], delay=4) == 0
assert trip_severity([3, 2, 0, 0, 4, 0, 4], delay=10) is None


# def safe_trip(depths, max_iters=int(1e6)):
#     for n in range(max_iters):
#         if trip_severity(depths, delay=n) is None:
#             return n
#     else:
#         return None


# assert safe_trip([3, 2, 0, 0, 4, 0, 4]) == 10


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()

    lines = s.split('\n')
    depths = [list(map(int, line.split(': '))) for line in lines]
    depths = {e[0]: e[1] for e in depths}
    depths = array_from_sparse_dict(depths)
    print(trip_severity(depths))
    # print(safe_trip(depths))

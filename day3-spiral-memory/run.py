#!/usr/bin/env python3

import itertools


def distances_to_center():
    """Generates all Manhattan distances to center of the spiral."""
    _min = 0
    _max = 1

    yield 0

    while True:
        _min += 1
        yield from range(_max, _min, -1)
        _max += 1
        yield from range(_min, _max,  1)

        yield from range(_max, _min, -1)
        yield from range(_min, _max,  1)

        yield from range(_max, _min, -1)
        yield from range(_min, _max,  1)

        yield from range(_max, _min, -1)
        _max += 1
        yield from range(_min, _max,  1)


def distance_to_center(n):
    """Return Manhattan distance to center of spiral of length <n>."""
    dist = distances_to_center()
    for _ in range(n - 1):
        next(dist)
    return next(dist)


def unwind(g, num):
    """Return <num> first elements from iterator <g> as array."""
    return [next(g) for _ in range(num)]


# print(unwind(distances_to_center(), 50))

assert distance_to_center(1) == 0
assert distance_to_center(2) == 1
assert distance_to_center(3) == 2
assert distance_to_center(4) == 1
assert distance_to_center(5) == 2
assert distance_to_center(6) == 1
assert distance_to_center(7) == 2
assert distance_to_center(8) == 1
assert distance_to_center(9) == 2
assert distance_to_center(10) == 3
assert distance_to_center(11) == 2
assert distance_to_center(12) == 3
assert distance_to_center(13) == 4
assert distance_to_center(14) == 3
assert distance_to_center(15) == 2
assert distance_to_center(23) == 2
assert distance_to_center(1024) == 31


spiral_length = 277678
print(distance_to_center(spiral_length))


# -------------------------------------


from collections import defaultdict


def neighbourhood(p):
    """Returns 9 points belonging to neighbourhood of point <p>."""
    x, y = p

    return [
        p,
        (x+1, y+0),
        (x+1, y+1),
        (x+0, y+1),
        (x-1, y+1),
        (x-1, y+0),
        (x-1, y-1),
        (x+0, y-1),
        (x+1, y-1)
    ]


def runs():
    n = 1
    while True:
        yield n
        yield n
        n += 1


RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
NUMDIR = 4


def spiral_points(start_pos):
    run = runs()
    movements = next(run)

    direction = RIGHT
    pos = start_pos

    while True:
        yield pos

        x, y = pos

        if direction == RIGHT:
            pos = (x+1, y+0)
        elif direction == UP:
            pos = (x+0, y+1)
        elif direction == LEFT:
            pos = (x-1, y+0)
        elif direction == DOWN:
            pos = (x+0, y-1)

        movements -= 1

        if movements <= 0:
            direction += 1
            direction %= NUMDIR
            movements = next(run)


def neighbour_sums():
    """Walks through the spiral, generating sums out of neighbouring points."""
    value_map = defaultdict(int)
    spiral_pos = spiral_points((0, 0))

    pos = next(spiral_pos)
    value_map[pos] = 1

    while True:
        value_map[pos] = sum(value_map[p] for p in neighbourhood(pos))
        yield value_map[pos]
        pos = next(spiral_pos)


actual = neighbourhood((0, 0))
expected = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
assert actual == expected


def assert_next(iter, expected):
    actual = next(iter)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


run = runs()
assert_next(run, 1)
assert_next(run, 1)
assert_next(run, 2)
assert_next(run, 2)
assert_next(run, 3)

pts = spiral_points((0, 0))
assert_next(pts, (+0, +0))
assert_next(pts, (+1, +0))
assert_next(pts, (+1, +1))
assert_next(pts, (+0, +1))
assert_next(pts, (-1, +1))
assert_next(pts, (-1, +0))
assert_next(pts, (-1, -1))
assert_next(pts, (+0, -1))
assert_next(pts, (+1, -1))
assert_next(pts, (+2, -1))
assert_next(pts, (+2, +0))
assert_next(pts, (+2, +1))
assert_next(pts, (+2, +2))

sums = neighbour_sums()
assert_next(sums, 1)
assert_next(sums, 1)
assert_next(sums, 2)
assert_next(sums, 4)
assert_next(sums, 5)
assert_next(sums, 10)
assert_next(sums, 11)
assert_next(sums, 23)
assert_next(sums, 25)
assert_next(sums, 26)


def puzzle(spiral_length):
    for s in neighbour_sums():
        if s > spiral_length:
            return s


spiral_length = 277678
print(puzzle(spiral_length))

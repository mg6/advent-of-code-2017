#!/usr/bin/env python3


def load_grid(s):
    s = s.strip()
    width, height = s.find('\n'), s.count('\n') + 1
    assert width == height
    grid = {(x, y)
            for y, line in enumerate(s.split('\n'), start=-height // 2 + 1)
            for x, c in enumerate(line, start=-width // 2 + 1)
            if c == '#'}
    return grid


def bursts(grid, stop):
    directions = (
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    )
    num_dirs = len(directions)
    pos = (0, 0)
    dir = (0, -1)
    grid = load_grid(grid)

    for _ in range(stop):
        idx = (directions.index(dir) + (1 if pos in grid else -1)) % num_dirs
        dir = directions[idx]
        try:
            grid.remove(pos)
            yield 0
        except KeyError:
            grid.add(pos)
            yield 1
        pos = tuple(x + y for x, y in zip(pos, dir))
        yield grid


actual = load_grid(".##\n..#\n...")
expected = {(0, -1), (1, -1), (1, 0)}
assert actual == expected, actual

actual = load_grid("..#\n#..\n...")
expected = {(1, -1), (-1, 0)}
assert actual == expected, actual

burst = bursts("""
..#
#..
...
""", stop=1000)
grid = filter(lambda e: type(e) == set, burst)

actual = next(grid)
expected = {(-1, 0), (0, 0), (1, -1)}
assert actual == expected, actual

actual = next(grid)
expected = {(0, 0), (1, -1)}
assert actual == expected, actual

burst = bursts("""
..#
#..
...
""", stop=7)
actual = sum(v for v in burst if type(v) == int)
assert actual == 5

burst = bursts("""
..#
#..
...
""", stop=70)
actual = sum(v for v in burst if type(v) == int)
assert actual == 41

burst = bursts("""
..#
#..
...
""", stop=10000)
actual = sum(v for v in burst if type(v) == int)
assert actual == 5587


if __name__ == '__main__':
    with open('input') as f:
        grid = f.read().strip()

    burst = bursts(grid, stop=10000)
    infections = sum(v for v in burst if type(v) == int)
    print(infections)

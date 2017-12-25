#!/usr/bin/env python3


from collections import deque
from functools import reduce


def hash_states(size=256):
    state = deque(range(size))
    skip_size = 0
    at = 0

    while True:
        rev_length = yield

        if rev_length > 1:
            state.rotate(-at)
            for v in [state.popleft() for _ in range(rev_length)]:
                state.appendleft(v)
            state.rotate(at)

        yield state
        at += rev_length + skip_size
        skip_size += 1


def knot_hash(lengths, size=256, rounds=1):
    h = hash_states(size)
    state = None

    for _ in range(rounds):
        for length in lengths:
            next(h)
            state = h.send(length)

    return state


def puzzle_multiply(lengths, size=256):
    a, b, *_ = knot_hash(lengths, size)
    return a * b


def sparse_hash(lengths, size=256, rounds=64):
    std_suffixes = [17, 31, 73, 47, 23]
    return list(knot_hash(lengths + std_suffixes, size, rounds))


def xor_block(state):
    return reduce(lambda a, b: a ^ b, state, 0)


def xor_blocks(state, numblocks=16, blocklen=16):
    blocks = [state[n*blocklen:(n+1)*blocklen] for n in range(numblocks)]
    return [xor_block(b) for b in blocks]


def dense_hash(lengths, size=256, rounds=64):
    return xor_blocks(sparse_hash(lengths, size, rounds))


def to_hex(nums):
    return ''.join('%02x' % n for n in nums)


def puzzle_hash(msg):
    msg = list(map(ord, msg))
    return to_hex(dense_hash(msg))


def assert_send(coroutine, value, expected):
    next(coroutine)
    actual = coroutine.send(value)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


h = hash_states(5)
assert_send(h, 3, deque([2, 1, 0, 3, 4]))
assert_send(h, 4, deque([4, 3, 0, 1, 2]))
assert_send(h, 1, deque([4, 3, 0, 1, 2]))
assert_send(h, 5, deque([3, 4, 2, 1, 0]))

assert puzzle_multiply([3, 4, 1, 5], size=5) == 12

assert xor_block([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]) == \
       65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22 == 64
assert xor_blocks([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22], numblocks=1) == [64]
assert xor_blocks([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22], numblocks=16, blocklen=1) == \
       [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]
assert xor_blocks([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22], numblocks=8, blocklen=2) == \
       [65 ^ 27, 9 ^ 1, 4 ^ 3, 40 ^ 50, 91 ^ 7, 6 ^ 0, 2 ^ 5, 68 ^ 22]

assert to_hex([]) == ''
assert to_hex([32]) == '20'
assert to_hex([64, 7, 255]) == '4007ff'
assert to_hex([1, 2, 3, 4]) == '01020304'

assert puzzle_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert puzzle_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert puzzle_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert puzzle_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'


def hex_to_bin(s):
    return ''.join('{0:04b}'.format(int(x, base=16)) for x in s)


assert hex_to_bin('0') == '0000'
assert hex_to_bin('1') == '0001'
assert hex_to_bin('e') == '1110'
assert hex_to_bin('f') == '1111'
assert hex_to_bin('a0c2017') == '1010000011000010000000010111'


def count_char(s, char):
    return sum(1 for c in s if c == char)


assert count_char('', '1') == 0
assert count_char('0', '1') == 0
assert count_char('02', '1') == 0
assert count_char('1', '1') == 1
assert count_char('11', '1') == 2


def array_grid_from_string(s):
    return [list(map(int, line)) for line in s.strip().split('\n')]


assert array_grid_from_string("""
0
""") == [[0]]

assert array_grid_from_string("""
00
00
""") == [[0, 0], [0, 0]]

assert array_grid_from_string("""
01
23
""") == [[0, 1], [2, 3]]


def flood(grid, x, y, visited=None, high=1, low=0):
    if not visited:
        visited = set()

    visited.add((x, y))

    if x >= 0 and y >= 0 and grid[x][y] == high:
        grid[x][y] = low
    else:
        return grid

    for x, y in ((x+0, y+1), (x+1, y+0), (x+0, y-1), (x-1, y+0)):
        try:
            if (x, y) not in visited:
                flood(grid, x, y, visited)
        except IndexError:
            pass

    return grid


assert flood([[0]], 0, 0) == [[0]]
assert flood([[1]], 0, 0) == [[0]]
assert flood([[2]], 0, 0) == [[2]]
assert flood([[1, 1], [1, 1]], 0, 0) == [[0, 0], [0, 0]]
assert flood([[1, 1], [1, 1]], 1, 1) == [[0, 0], [0, 0]]
assert flood([[1, 1], [1, 2]], 0, 0) == [[0, 0], [0, 2]]
assert flood([[1, 1], [1, 2]], 1, 1) == [[1, 1], [1, 2]]
assert flood([[1, 1, 1], [1, 2, 1], [1, 1, 1]], 0, 0) == [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
assert flood([[1, 1, 1], [1, 2, 1], [1, 1, 1]], 2, 2) == [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
assert flood([[1, 1, 1], [1, 2, 1], [1, 1, 1]], 0, 2) == [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
assert flood([[1, 0, 1], [1, 0, 1], [1, 0, 1]], 0, 0) == [[0, 0, 1], [0, 0, 1], [0, 0, 1]]
assert flood([[1, 0, 1], [0, 0, 0], [1, 0, 1]], 0, 0) == [[0, 0, 1], [0, 0, 0], [1, 0, 1]]


def grid_find(grid, value):
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == value:
                return i, j
    return None


assert grid_find([[0]], 0) == (0, 0)
assert grid_find([[0]], 1) is None
assert grid_find([[0, 0], [0, 1]], 1) == (1, 1)


def count_regions(s):
    grid = array_grid_from_string(s)
    count = 0

    while True:
        p = grid_find(grid, 1)
        if not p:
            break
        count += 1
        x, y = p
        flood(grid, x, y)

    return count


assert count_regions("""
0
""") == 0

assert count_regions("""
1
""") == 1

assert count_regions("""
11
11
""") == 1

assert count_regions("""
111
101
111
""") == 1

assert count_regions("""
010
111
010
""") == 1

assert count_regions("""
101
101
101
""") == 2

assert count_regions("""
101
010
101
""") == 5


if __name__ == '__main__':
    inp = 'vbqugkhl'
    grid = '\n'.join(hex_to_bin(puzzle_hash('{}-{}'.format(inp, n)))
                     for n in range(128))
    print(count_char(grid, '1'))
    print(count_regions(grid))

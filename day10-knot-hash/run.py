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


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()
        lengths = list(map(int, s.split(',')))
        print(puzzle_multiply(lengths))
        print(puzzle_hash(s))

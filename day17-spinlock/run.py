#!/usr/bin/env python3


from itertools import count, islice


def spinlock(step):
    state = [0]
    at = 0

    for n in count(1):
        yield state, at
        at = (at + step) % n
        at += 1
        state.insert(at, n)


s = spinlock(3)

state, at = next(s)
assert list(state) == [0]
assert at == 0

state, at = next(s)
assert list(state) == [0, 1], state
assert at == 1

state, at = next(s)
assert list(state) == [0, 2, 1], state
assert at == 1

state, at = next(s)
assert list(state) == [0, 2, 3, 1], state
assert at == 2

state, at = next(s)
assert list(state) == [0, 2, 4, 3, 1], state
assert at == 2

state, at = next(s)
assert list(state) == [0, 5, 2, 4, 3, 1], state
assert at == 1

state, at = next(s)
assert list(state) == [0, 5, 2, 4, 3, 6, 1], state
assert at == 5

state, at = next(s)
assert list(state) == [0, 5, 7, 2, 4, 3, 6, 1], state
assert at == 2

state, at = next(s)
assert list(state) == [0, 5, 7, 2, 4, 3, 8, 6, 1], state
assert at == 6

state, at = next(s)
assert list(state) == [0, 9, 5, 7, 2, 4, 3, 8, 6, 1], state
assert at == 1

s = spinlock(3)
state, at = next(islice(s, 2017, 2018))
assert state[at + 1] == 638

puzzle_input = 376
s = spinlock(puzzle_input)
state, at = next(islice(s, 2017, 2018))
print(state[at + 1])

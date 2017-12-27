#!/usr/bin/env python3


from collections import deque
from itertools import count, islice


def spinlock(step):
    state = deque([0])
    for n in count(1):
        yield state
        state.rotate(-step)
        state.append(n)


s = spinlock(3)

state = next(s)
assert list(state) == [0], state

state = next(s)
assert list(state) == [0, 1], state

state = next(s)
assert list(state) == [1, 0, 2], state

state = next(s)
assert list(state) == [1, 0, 2, 3], state

state = next(s)
assert list(state) == [3, 1, 0, 2, 4], state

state = next(s)
assert list(state) == [2, 4, 3, 1, 0, 5], state

state = next(s)
assert list(state) == [1, 0, 5, 2, 4, 3, 6], state

state = next(s)
assert list(state) == [2, 4, 3, 6, 1, 0, 5, 7], state

state = next(s)
assert list(state) == [6, 1, 0, 5, 7, 2, 4, 3, 8], state

state = next(s)
assert list(state) == [5, 7, 2, 4, 3, 8, 6, 1, 0, 9], state

s = spinlock(3)
state = next(islice(s, 2017, 2018))
assert state[0] == 638

puzzle_input = 376
s = spinlock(puzzle_input)
state = next(islice(s, 2017, 2018))
print(state[0])

s = spinlock(puzzle_input)
state = next(islice(s, 50000000, 50000000+1))
print(state[state.index(0) + 1])

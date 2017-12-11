#!/usr/bin/env python3

import itertools


increment = lambda offset: 1

strange_jump = lambda offset: -1 if offset > 2 else 1


def cpu_states(initial_state, increase_func, at=0):
    pos = at

    # Give this man a medal -- make a COPY of input data.
    # <https://www.reddit.com/r/adventofcode/comments/7hr5ya/psa2017_day_5_part_2_offset_of_three_or_more_is/dqtg5pz/>
    state = initial_state[:]
    num_instructions = len(state)

    while True:
        yield state, pos

        if 0 <= pos < num_instructions:
            old_pos = pos
            offset = state[pos]
            pos += offset
            state[old_pos] += increase_func(offset)


def puzzle(initial_state, increase_func=increment):
    num_instructions = len(initial_state)
    state = cpu_states(initial_state, increase_func=increase_func)

    for step in itertools.count():
        cur_state, pos = next(state)

        if not (0 <= pos < num_instructions):
            return step, cur_state


def assert_next(iter, expected):
    actual = next(iter)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


assert increment(0) == 1

assert all(strange_jump(n) == +1 for n in range(-10, 3))
assert all(strange_jump(n) == -1 for n in range(3, 10))

state = cpu_states([0, 3, 0, 1, -3], increase_func=increment, at=0)
assert_next(state, ([0, 3, 0, 1, -3], 0))
assert_next(state, ([1, 3, 0, 1, -3], 0))
assert_next(state, ([2, 3, 0, 1, -3], 1))
assert_next(state, ([2, 4, 0, 1, -3], 4))
assert_next(state, ([2, 4, 0, 1, -2], 1))
assert_next(state, ([2, 5, 0, 1, -2], 5))
assert_next(state, ([2, 5, 0, 1, -2], 5))
assert_next(state, ([2, 5, 0, 1, -2], 5))

state = cpu_states([2, 0], increase_func=increment, at=0)
assert_next(state, ([2, 0], 0))
assert_next(state, ([3, 0], 2))

state = cpu_states([0, -2], increase_func=increment, at=1)
assert_next(state, ([0, -2], 1))
assert_next(state, ([0, -1], -1))

steps, end_state = puzzle([0, 3, 0, 1, -3], increase_func=increment)
assert steps == 5
assert end_state == [2, 5, 0, 1, -2]

steps, end_state = puzzle([2, 0], increase_func=increment)
assert steps == 1
assert end_state == [3, 0]

steps, end_state = puzzle([0, 3, 0, 1, -3], increase_func=strange_jump)
assert steps == 10
assert end_state == [2, 3, 2, 3, -1]


if __name__ == '__main__':
    with open('input') as f:
        lines = f.readlines()
        initial_state = [int(line.strip()) for line in lines]

        step, *_ = puzzle(initial_state, increase_func=increment)
        print(step)

        step, *_ = puzzle(initial_state, increase_func=strange_jump)
        print(step)

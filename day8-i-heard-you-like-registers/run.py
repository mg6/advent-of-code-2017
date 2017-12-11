#!/usr/bin/env python3

from collections import defaultdict


def valid_cond(a, op, b):
    assert type(a) == int
    assert type(b) == int

    if op in ('<', '>', '<=', '>=', '==', '!='):
        return eval('a %s b' % op)
    else:
        raise ValueError('Unsupported operation: %s' % op)


def register_states(program):
    state = defaultdict(int)

    for instr in program:
        reg, op, delta, _, cond_reg, cond_op, cond_val = instr.split()
        delta = int(delta)
        cond_val = int(cond_val)

        if valid_cond(state[cond_reg], cond_op, cond_val):
            if op == 'inc':
                state[reg] += delta
            elif op == 'dec':
                state[reg] -= delta
            else:
                raise ValueError('Unsupported operation: %s' % op)

        yield state


def max_register_value(program):
    states = register_states(program)
    overall_max = 0

    while True:
        try:
            state = next(states)
            overall_max = max(overall_max, max(state.values()))
        except StopIteration:
            return max(state.values()), overall_max


def assert_next(iter, expected):
    actual = next(iter)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


program = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""".strip().split('\n')

assert valid_cond(3, '<',  6)
assert not valid_cond(3, '>=', 6)
assert valid_cond(3, '<=', 6)
assert not valid_cond(3, '>',  6)
assert valid_cond(3, '!=', 6)
assert not valid_cond(3, '==', 6)

try:
    valid_cond(3, '<=>', 6)
except ValueError:
    pass
else:
    assert False, 'Should throw for unsupported operation'

states = register_states(program)
assert_next(states, {'a': 0})                       # b inc 5 if a > 1
assert_next(states, {'a': 1, 'b': 0})               # a inc 1 if b < 5
assert_next(states, {'a': 1, 'b': 0, 'c': 10})      # c dec -10 if a >= 1
assert_next(states, {'a': 1, 'b': 0, 'c': -10})     # c inc -20 if c == 10

try:
    next(states)
except StopIteration:
    pass
else:
    assert False, 'Should throw past last state'

assert max_register_value(program) == (1, 10)


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip().split('\n')
        print(max_register_value(s))

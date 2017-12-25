#!/usr/bin/env python3

from collections import defaultdict
from itertools import count, islice
import re


def read_rules(s):
    initial_state = None
    checksum_after = None
    state = None
    value = None
    rules = {}

    for line in s.strip().split('\n'):
        if not line:
            pass
        elif '    - Continue with state ' in line:
            new_state = line[len('    - Continue with state ')]
            rules[state][value]['state'] = new_state
        elif '    - Move one slot to the ' in line:
            direc = line[len('    - Move one slot to the ')]
            rules[state][value]['move'] = 1 if direc == 'r' else -1
        elif '    - Write the value ' in line:
            write = int(line[len('    - Write the value ')])
            rules[state][value]['write'] = write
        elif '  If the current value is ' in line:
            value = int(line[len('  If the current value is ')])
        elif 'In state ' in line:
            state = line[len('In state ')]
            if state not in rules:
                rules[state] = {0: {}, 1: {}}
        elif 'Perform a diagnostic checksum after ' in line:
            m = re.search(r'\d+', line)
            checksum_after = int(m.group(0))
        elif 'Begin in state ' in line:
            initial_state = line[len('Begin in state ')]

    return initial_state, checksum_after, rules


def turing_machine(initial_state, rules, checksum_after):
    at = 0
    tape = defaultdict(int, {at: 0, 'state': initial_state})

    for n in count():
        if n == checksum_after:
            yield sum(v for k, v in tape.items() if k != 'state')

        rule = rules[tape['state']][tape[at]]
        tape[at] = rule['write']
        at += rule['move']
        tape[at] = tape[at]
        tape['state'] = rule['state']
        yield tape


initial_state, checksum_after, rules = read_rules("""
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
""")

expected = {
    'A': {
        0: {
            'write': 1,
            'move': 1,
            'state': 'B',
        },
        1: {
            'write': 0,
            'move': -1,
            'state': 'B',
        }
    },
    'B': {
        0: {
            'write': 1,
            'move': -1,
            'state': 'A',
        },
        1: {
            'write': 1,
            'move': 1,
            'state': 'A',
        },
    },
}

assert initial_state == 'A'
assert checksum_after == 6
assert rules == expected

tm = turing_machine('A', rules, checksum_after=6)

actual = next(tm)
expected = {0: 1, 1: 0, 'state': 'B'}
assert actual == expected, actual

actual = next(tm)
expected = {0: 1, 1: 1, 'state': 'A'}
assert actual == expected, actual

actual = next(tm)
expected = {-1: 0, 0: 0, 1: 1, 'state': 'B'}
assert actual == expected, actual

actual = next(tm)
expected = {-2: 0, -1: 1, 0: 0, 1: 1, 'state': 'A'}
assert actual == expected, actual

actual = next(tm)
expected = {-2: 1, -1: 1, 0: 0, 1: 1, 'state': 'B'}
assert actual == expected, actual

actual = next(tm)
expected = {-2: 1, -1: 1, 0: 0, 1: 1, 'state': 'A'}
assert actual == expected, actual

actual = next(tm)
expected = 3
assert actual == expected, actual

tm = turing_machine('A', rules, checksum_after=6)
actual = next(islice(tm, 6, 7))
expected = 3
assert actual == expected, actual


if __name__ == '__main__':
    with open('input') as f:
        rules = f.read().strip()

    initial_state, checksum_after, rules = read_rules(rules)
    tm = turing_machine(initial_state, rules, checksum_after=checksum_after)
    print(next(islice(tm, checksum_after, checksum_after + 1)))

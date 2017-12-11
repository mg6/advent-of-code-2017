#!/usr/bin/env python3


def parse_garbage(stream):
    stream = iter(stream)
    while True:
        try:
            c = next(stream)
        except StopIteration:
            return
        else:
            if c == '!':
                next(stream)
            elif c == '>':
                return
            else:
                yield c


def parse_stream(stream):
    stream = iter(stream)
    while True:
        try:
            c = next(stream)
        except StopIteration:
            return
        else:
            if c == '{':
                yield list(parse_stream(stream))
            elif c == '}':
                raise StopIteration
            elif c == '<':
                garbage = ''.join(parse_garbage(stream))
                yield garbage


def get_score(elem, score=0):
    children = sum(get_score(e, score=score+1) for e in elem if type(e) == list)
    return score + children


def count_garbage(elem):
    if type(elem) == str:
        return len(elem)
    else:
        return sum(count_garbage(e) for e in elem)


def assert_next(iter, expected):
    actual = next(iter)
    assert actual == expected, "expected %s, got %s" % (expected, actual)


stream = parse_stream('')
try:
    next(stream)
except StopIteration:
    pass
else:
    assert False, 'Should immediately finish on empty stream'

assert_next(parse_stream('<>'), '')
assert_next(parse_stream('<random characters>'), 'random characters')
assert_next(parse_stream('<<<<>'), '<<<')
assert_next(parse_stream('<{!>}>'), '{}')
assert_next(parse_stream('<!!>'), '')
assert_next(parse_stream('<!!!>>'), '')
assert_next(parse_stream('<{o"i!a,<{i<a>'), '{o"i,<{i<a')

assert_next(parse_stream('{}'), [])
assert_next(parse_stream('{{{}}}'), [[[]]])
assert_next(parse_stream('{{}, {}}'), [[], []])
assert_next(parse_stream('{{{},{},{{}}}}'), [[[], [], [[]]]])

stream = parse_stream('{<a>,<a>,<a>,<a>}')
assert_next(stream, ['a', 'a', 'a', 'a'])

stream = parse_stream('{{<ab>},{<ab>},{<ab>},{<ab>}}')
assert_next(stream, [['ab'], ['ab'], ['ab'], ['ab']])

stream = parse_stream('{{<!!>},{<!!>},{<!!>},{<!!>}}')
assert_next(stream, [[''], [''], [''], ['']])

stream = parse_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}')
assert_next(stream, [['a},{<a},{<a},{<ab']])

assert get_score(parse_stream('{}')) == 1
assert get_score(parse_stream('{{{}}}')) == 6
assert get_score(parse_stream('{{},{}}')) == 5
assert get_score(parse_stream('{{{},{},{{}}}}')) == 16
assert get_score(parse_stream('{<a>,<a>,<a>,<a>}')) == 1
assert get_score(parse_stream('{{<ab>},{<ab>},{<ab>},{<ab>}}')) == 9
assert get_score(parse_stream('{{<!!>},{<!!>},{<!!>},{<!!>}}')) == 9
assert get_score(parse_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}')) == 3

assert count_garbage(parse_stream('<>')) == 0
assert count_garbage(parse_stream('<random characters>')) == 17
assert count_garbage(parse_stream('<<<<>')) == 3
assert count_garbage(parse_stream('<{!>}>')) == 2
assert count_garbage(parse_stream('<!!>')) == 0
assert count_garbage(parse_stream('<!!!>>')) == 0
assert count_garbage(parse_stream('<{o"i!a,<{i<a>')) == 10

assert count_garbage(parse_stream('{<>}')) == 0
assert count_garbage(parse_stream('{<random characters>}')) == 17
assert count_garbage(parse_stream('{{<random characters>}}')) == 17
assert count_garbage(parse_stream('{<random characters>, <abc>}')) == 20


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()
        tree = list(parse_stream(s))
        print(get_score(tree))
        print(count_garbage(tree))

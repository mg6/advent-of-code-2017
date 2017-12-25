#!/usr/bin/env python3


from collections import deque


def dance(progs='abcdefghijklmnop'):
    progs = deque((progs))

    while True:
        move = yield
        if move[0] == 's':      # spin (sX)
            progs.rotate(int(move[1:]))
        elif move[0] == 'x':    # exchange (xA/B)
            a, b = map(int, move[1:].split('/'))
            progs[a], progs[b] = progs[b], progs[a]
        elif move[0] == 'p':    # partner (pA/B)
            a, b = move[1:].split('/')
            a, b = progs.index(a), progs.index(b)
            progs[a], progs[b] = progs[b], progs[a]
        yield ''.join(progs)


d = dance('abcde')
next(d)
assert d.send('s1') == 'eabcd'
next(d)
assert d.send('x3/4') == 'eabdc'
next(d)
assert d.send('pe/b') == 'baedc'


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()
        moves = s.split(',')

    d = dance()

    for move in moves:
        next(d)
        progs = d.send(move)

    print(progs)

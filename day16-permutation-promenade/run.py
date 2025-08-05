#!/usr/bin/env python3


from collections import deque

START = "abcdefghijklmnop"


def dance(progs=START):
    progs = deque(progs)

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


def test_dance():
    d = dance("abcde")

    next(d)
    assert d.send("s1") == "eabcd"

    next(d)
    assert d.send("x3/4") == "eabdc"

    next(d)
    assert d.send("pe/b") == "baedc"


if __name__ == '__main__':
    NUM_ITERS = 1_000_000_000

    with open('input') as f:
        s = f.read().strip()
        moves = s.split(',')

    d = dance()

    i = 0
    while i < NUM_ITERS:
        i += 1

        # execute once
        for move in moves:
            next(d)
            progs = d.send(move)

        if i == 1:
            # part 1
            print(progs, i)

        elif progs == START:
            # cycle detected
            print(progs, i)
            i = NUM_ITERS - NUM_ITERS % i

        elif i >= NUM_ITERS:
            # part 2
            print(progs, i)
            break

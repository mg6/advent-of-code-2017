#!/usr/bin/env python3


from collections import namedtuple
from itertools import islice, groupby
from operator import itemgetter

particle = namedtuple("particle", "p v a")


def tick(p):
    a = p.a
    v = tuple(v + a[i] for i, v in enumerate(p.v))
    p = tuple(p + v[i] for i, p in enumerate(p.p))
    return particle(p, v, a)


def manhattan_distance(p):
    return sum(map(abs, p.p))


def particle_from_string(line):
    p, v, a = line.split(', ')
    p = tuple(int(v) for v in p[3:-1].split(','))
    v = tuple(int(v) for v in v[3:-1].split(','))
    a = tuple(int(v) for v in a[3:-1].split(','))
    return particle(p, v, a)


def simulate(particles):
    while True:
        particles = [tick(p) for p in particles]
        yield particles


def part_p(particle):
    return particle.p


def simulate_with_collision(particles):
    while True:
        particles = [tick(p) for p in particles]
        particles = list(remove_duplicated(
            particles, sort_key=part_p, groupby_key=part_p))
        yield particles


def remove_duplicated(it, sort_key=None, groupby_key=None):
    it = sorted(it, key=sort_key)
    for k, g in groupby(it, groupby_key):
        g = list(g)
        if len(g) == 1:
            yield from g


p1 = particle(p=(3, 0, 0), v=(2, 0, 0), a=(-1, 0, 0))
p2 = particle(p=(4, 0, 0), v=(0, 0, 0), a=(-2, 0, 0))

assert p1.p == (3, 0, 0)
assert p1.v == (2, 0, 0)
assert p1.a == (-1, 0, 0)

p1 = tick(p1)
assert p1.p == (4, 0, 0)
assert p1.v == (1, 0, 0)
assert p1.a == (-1, 0, 0)

p1 = tick(p1)
assert p1.p == (4, 0, 0)
assert p1.v == (0, 0, 0)
assert p1.a == (-1, 0, 0)

p1 = tick(p1)
assert p1.p == (3, 0, 0)
assert p1.v == (-1, 0, 0)
assert p1.a == (-1, 0, 0)

z3 = (0, 0, 0)

p = particle(p=(0, 0, 0), v=z3, a=z3)
assert manhattan_distance(p) == 0

p = particle(p=(1, 2, 8), v=z3, a=z3)
assert manhattan_distance(p) == 11

p = particle(p=(-5, 2, 3), v=z3, a=z3)
assert manhattan_distance(p) == 10

actual = particle_from_string('p=<2395,-194,549>, v=<-141,23,-78>, a=<-9,-1,5>')
expected = particle(p=(2395, -194, 549), v=(-141, 23, -78), a=(-9, -1, 5))
assert actual == expected

actual = list(remove_duplicated([1, 2, 3, 4]))
expected = [1, 2, 3, 4]
assert actual == expected, actual

actual = list(remove_duplicated([0, 0, 3, 4]))
expected = [3, 4]
assert actual == expected, actual

actual = list(remove_duplicated([1, 0, 0, 4]))
expected = [1, 4]
assert actual == expected, actual

actual = list(remove_duplicated([1, 2, 0, 0]))
expected = [1, 2]
assert actual == expected, actual


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip().split('\n')

    particles = [particle_from_string(line) for line in s]

    sim = next(islice(simulate(particles), 1000, 1001))
    distances = [manhattan_distance(p) for p in sim]
    min_idx, min_dist = min(enumerate(distances), key=itemgetter(1))
    print(min_idx, min_dist)

    sim = next(islice(simulate_with_collision(particles), 1000, 1001))
    print(len(sim))

#!/usr/bin/env python3


from functools import lru_cache
from itertools import islice
from math import sqrt


def get_grid_size(grid):
    """Return grid edge size."""
    if not grid:
        return 0

    pos = grid.find('\n')
    if pos < 0:
        return 1

    return pos


@lru_cache(maxsize=None)
def flip_h(grid):
    """Flip grid horizontally."""
    return '\n'.join(''.join(reversed(line)) for line in grid.split('\n'))


@lru_cache(maxsize=None)
def flip_v(grid):
    """Flip grid vertically."""
    return '\n'.join(reversed(grid.split('\n')))


@lru_cache(maxsize=None)
def rotate(grid):
    """Rotate grid 90 deg to the right."""
    rows = grid.split('\n')
    return '\n'.join(''.join(chars) for chars in zip(*reversed(rows)))


def all_rotations(grid):
    """Return all rotations of grid."""
    r0 = grid
    r1 = rotate(r0)
    r2 = rotate(r1)
    r3 = rotate(r2)
    return {r0, r1, r2, r3}


def all_permutations(grid):
    """Return all possible permutations of given grid."""
    return {*all_rotations(grid), *all_rotations(flip_v(grid))}


@lru_cache(maxsize=None)
def normalize(grid):
    """Out of all grid's permutations, return alphabetically first."""
    permutations = all_permutations(grid)
    return min(permutations)


def apply_rule(rules, chunk):
    """Return matching rule's output for given chunk."""
    chunk = normalize(chunk)
    if chunk in rules:
        return rules[chunk]
    else:
        raise ValueError("Chunk does not match rules:\n%s" % chunk)


def each_n(iterable, n):
    """Iterate iterable with n-tuples."""
    a = iter(iterable)
    return zip(*[a] * n)


def split_grid_mod2(grid):
    """Generate all 2x2 chunks from grid."""
    for line1, line2 in each_n(grid.split('\n'), n=2):
        iterable = zip(line1, line2)
        for a, b in each_n(iterable, n=2):
            yield "{}{}\n{}{}".format(a[0], b[0],
                                      a[1], b[1])


def split_grid_mod3(grid):
    """Generate all 3x3 chunks from grid."""
    for line1, line2, line3 in each_n(grid.split('\n'), n=3):
        iterable = zip(line1, line2, line3)
        for a, b, c in each_n(iterable, n=3):
            yield "{}{}{}\n{}{}{}\n{}{}{}".format(a[0], b[0], c[0],
                                                  a[1], b[1], c[1],
                                                  a[2], b[2], c[2])


def split_grid(grid):
    """Split grid into chunks of 2x2 or 3x3 size."""
    size = get_grid_size(grid)
    if size % 2 == 0:
        yield from split_grid_mod2(grid)
    elif size % 3 == 0:
        yield from split_grid_mod3(grid)
    else:
        raise ValueError('Grid size is not divisible by 2 nor 3')


def combine_grid(chunks):
    """Combine grid back from chunk list."""
    chunks = list(chunks)
    assert abs(sqrt(len(chunks)) % 1) < 0.0001
    size = round(sqrt(len(chunks)))

    if size == 1:
        yield chunks[0]
        return

    for row in each_n(chunks, n=size):
        row = [chunk.split('\n') for chunk in row]
        yield from (''.join(elem) for elem in zip(*row))


def grid_states(rules, grid=None):
    """Generate grid states according to fractal rules."""
    if grid is None:
        grid = ".#.\n..#\n###"

    while True:
        grid = '\n'.join(combine_grid(apply_rule(rules, chunk)
                                      for chunk in split_grid(grid)))
        yield grid


assert get_grid_size("") == 0
assert get_grid_size(".") == 1
assert get_grid_size("..\n..") == 2
assert get_grid_size("...\n...\n...") == 3


actual = flip_h("##\n.#")
expected = "##\n#."
assert actual == expected, actual

actual = flip_h("##.\n.#.\n..#")
expected = ".##\n.#.\n#.."
assert actual == expected, actual


actual = flip_v("##\n.#")
expected = ".#\n##"
assert actual == expected, actual

actual = flip_v("##.\n.#.\n..#")
expected = "..#\n.#.\n##."
assert actual == expected, actual


actual = rotate(".")
expected = "."
assert actual == expected, actual


actual = rotate(".#\n##")
expected = "#.\n##"
assert actual == expected, actual

actual = rotate("#.\n##")
expected = "##\n#."
assert actual == expected, actual

actual = rotate("##\n#.")
expected = "##\n.#"
assert actual == expected, actual

actual = rotate("##\n.#")
expected = ".#\n##"
assert actual == expected, actual

actual = rotate(rotate(rotate(rotate(".#\n##"))))
expected = ".#\n##"
assert actual == expected, actual


actual = rotate(".#.\n..#\n###")
expected = "#..\n#.#\n##."
assert actual == expected, actual

actual = rotate("#..\n#.#\n##.")
expected = "###\n#..\n.#."
assert actual == expected, actual

actual = rotate("###\n#..\n.#.")
expected = ".##\n#.#\n..#"
assert actual == expected, actual

actual = rotate(".##\n#.#\n..#")
expected = ".#.\n..#\n###"
assert actual == expected, actual

actual = rotate(rotate(rotate(rotate(".##\n#.#\n..#"))))
expected = ".##\n#.#\n..#"
assert actual == expected, actual


assert len(all_permutations(".")) == 1
assert len(all_permutations(".#\n##")) == 4
assert len(all_permutations(".#.\n..#\n###")) == 8


assert '#' < '.'
assert normalize(".#\n##") == "##\n#."
assert normalize(".#.\n..#\n###") == "###\n#..\n.#."


rules = {
    normalize("..\n.#"): "##.\n#..\n...",
    normalize(".#.\n..#\n###"): "#..#\n....\n....\n#..#",
}
assert apply_rule(rules, "..\n.#") == "##.\n#..\n..."
assert apply_rule(rules, ".#.\n..#\n###") == "#..#\n....\n....\n#..#"


assert list(each_n([], n=2)) == []
assert list(each_n([1, 2], n=2)) == [(1, 2)]
assert list(each_n([1, 2, 3, 4, 5, 6], n=2)) == [(1, 2), (3, 4), (5, 6)]


assert list(each_n([], n=3)) == []
assert list(each_n([1, 2, 3], n=3)) == [(1, 2, 3)]
assert list(each_n([1, 2, 3, 4, 5, 6], n=3)) == [(1, 2, 3), (4, 5, 6)]


actual = list(split_grid_mod2(".#\n##"))
expected = [".#\n##"]
assert actual == expected, actual

actual = list(split_grid_mod2("..##\n..##\n.##.\n#.##"))
expected = ["..\n..", "##\n##", ".#\n#.", "#.\n##"]
assert actual == expected, actual


actual = list(split_grid_mod3(".#.\n..#\n###"))
expected = [".#.\n..#\n###"]
assert actual == expected, actual

# ...|###
# ...|###
# ...|###
# ---+---
# ..#|.#.
# .#.|..#
# #..|###

actual = list(split_grid_mod3("...###\n...###\n...###\n..#.#.\n.#...#\n#..###"))
expected = ["...\n...\n...", "###\n###\n###", "..#\n.#.\n#..", ".#.\n..#\n###"]
assert actual == expected, actual


actual = list(split_grid(".#\n##"))
expected = [".#\n##"]
assert actual == expected, actual

actual = list(split_grid("..##\n..##\n.##.\n#.##"))
expected = ["..\n..", "##\n##", ".#\n#.", "#.\n##"]
assert actual == expected, actual

actual = list(split_grid(".#.\n..#\n###"))
expected = [".#.\n..#\n###"]
assert actual == expected, actual

# ..|.#|##
# ..|.#|##
# --+--+--
# ..|.#|##
# ..|#.|#.
# --+--+--
# .#|..|.#
# #.|.#|##

actual = list(split_grid("...###\n...###\n...###\n..#.#.\n.#...#\n#..###"))
expected = ["..\n..", ".#\n.#", "##\n##",
            "..\n..", ".#\n#.", "##\n#.",
            ".#\n#.", "..\n.#", ".#\n##"]
assert actual == expected, actual


actual = '\n'.join(combine_grid([".", "#", "#", "."]))
expected = ".#\n#."
assert actual == expected, actual

actual = '\n'.join(combine_grid(["..\n..", "##\n##", "##\n##", "..\n.."]))
expected = "..##\n..##\n##..\n##.."
assert actual == expected, actual


rules = {
    normalize("..\n.#"): "##.\n#..\n...",
    normalize(".#.\n..#\n###"): "#..#\n....\n....\n#..#",
}
states = grid_states(rules)

actual = next(states)
expected = "#..#\n....\n....\n#..#"
assert actual == expected, actual

actual = next(states)
expected = "##.##.\n#..#..\n......\n##.##.\n#..#..\n......"
assert actual == expected, actual


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip().split('\n')

    rules = dict()
    for line in s:
        k, v = line.split(' => ')
        k = normalize(k.replace('/', '\n'))
        v = v.replace('/', '\n')
        rules[k] = v

    states = grid_states(rules)
    grid = next(islice(states, 4, 5))
    print(grid.count('#'))

    grid = next(islice(states, 12, 13))
    print(grid.count('#'))

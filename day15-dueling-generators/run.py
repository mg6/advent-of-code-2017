#!/usr/bin/env python3


def generator(factor, seed=0, modulus=2147483647, multiple_of=1):
    assert multiple_of != 0
    while True:
        seed *= factor
        seed %= modulus
        if multiple_of == 1 or seed % multiple_of == 0:
            yield seed


def judge(gen_a, gen_b, num_comparisons, bits=16):
    matched = 0
    mask = (1 << bits) - 1
    for _ in range(num_comparisons):
        a = next(gen_a) & mask
        b = next(gen_b) & mask
        if a == b:
            matched += 1
    return matched


gen_a = generator(16807, seed=65)
assert next(gen_a) == 1092455
assert next(gen_a) == 1181022009
assert next(gen_a) == 245556042
assert next(gen_a) == 1744312007
assert next(gen_a) == 1352636452

gen_b = generator(48271, seed=8921)
assert next(gen_b) == 430625591
assert next(gen_b) == 1233683848
assert next(gen_b) == 1431495498
assert next(gen_b) == 137874439
assert next(gen_b) == 285222916

gen_a = generator(16807, seed=65)
gen_b = generator(48271, seed=8921)
assert judge(gen_a, gen_b, 5) == 1

gen_a = generator(16807, seed=65)
gen_b = generator(48271, seed=8921)
assert judge(gen_a, gen_b, int(40e6)) == 588

gen_a = generator(16807, seed=591)
gen_b = generator(48271, seed=393)
print(judge(gen_a, gen_b, int(40e6)))


gen_a = generator(16807, seed=65, multiple_of=4)
assert next(gen_a) == 1352636452
assert next(gen_a) == 1992081072
assert next(gen_a) == 530830436
assert next(gen_a) == 1980017072
assert next(gen_a) == 740335192

gen_b = generator(48271, seed=8921, multiple_of=8)
assert next(gen_b) == 1233683848
assert next(gen_b) == 862516352
assert next(gen_b) == 1159784568
assert next(gen_b) == 1616057672
assert next(gen_b) == 412269392

gen_a = generator(16807, seed=65, multiple_of=4)
gen_b = generator(48271, seed=8921, multiple_of=8)
assert judge(gen_a, gen_b, 1056) == 1

gen_a = generator(16807, seed=65, multiple_of=4)
gen_b = generator(48271, seed=8921, multiple_of=8)
assert judge(gen_a, gen_b, int(5e6)) == 309

gen_a = generator(16807, seed=591, multiple_of=4)
gen_b = generator(48271, seed=393, multiple_of=8)
print(judge(gen_a, gen_b, int(5e6)))

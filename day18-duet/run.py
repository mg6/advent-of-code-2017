#!/usr/bin/env python3


from collections import defaultdict


def get_val(name, state):
    try:
        return int(name)
    except ValueError:
        return state[name]


def interpreter(prog, **kwargs):
    if type(prog) == str:
        prog = prog.strip().split('\n')

    regs = defaultdict(int)
    pc = 0

    while 0 <= pc < len(prog):
        instr = prog[pc]
        cmd, *args = instr.split()

        if cmd == 'set':
            reg, arg = args
            regs[reg] = get_val(arg, regs)
        elif cmd == 'add':
            reg, arg = args
            regs[reg] += get_val(arg, regs)
        elif cmd == 'mul':
            reg, arg = args
            regs[reg] *= get_val(arg, regs)
        elif cmd == 'mod':
            reg, arg = args
            regs[reg] %= get_val(arg, regs)
        elif cmd == 'jgz':
            arg, offset = args
            if get_val(arg, regs) > 0:
                pc += int(offset)
                continue
        elif cmd == 'snd':
            arg = get_val(args[0], regs)
            regs['snd'] = arg
        elif cmd == 'rcv':
            arg = get_val(args[0], regs)
            if arg != 0:
                regs['rcv'] = regs['snd']
                if 'rcv' in kwargs:
                    kwargs['rcv'](regs['rcv'])

        pc += 1

    return regs


actual = interpreter("""
set a 5
""")
expected = {'a': 5}
assert actual == expected, actual

actual = interpreter("""
set z 5
""")
expected = {'z': 5}
assert actual == expected, actual

actual = interpreter("""
set a 8
set a 5
""")
expected = {'a': 5}
assert actual == expected, actual

actual = interpreter("""
add a 8
""")
expected = {'a': 8}
assert actual == expected, actual

actual = interpreter("""
set a 8
mul a 2
""")
expected = {'a': 16}
assert actual == expected, actual

actual = interpreter("""
set a 8
mod a 3
""")
expected = {'a': 2}
assert actual == expected, actual

actual = interpreter("""
add a 1
jgz a 2
add a 1
""")
expected = {'a': 1}
assert actual == expected, actual

actual = interpreter("""
set a 8
add a -1
jgz a -1
""")
expected = {'a': 0}
assert actual == expected, actual

actual = interpreter("""
jgz 5 -1
""")
expected = {}
assert actual == expected, actual

actual = interpreter("""
set a 8
snd a
""")
expected = {'a': 8, 'snd': 8}
assert actual == expected, actual

actual = interpreter("""
snd 7
rcv 0
snd 6
""")
expected = {'snd': 6}
assert actual == expected, actual

actual = interpreter("""
snd 7
rcv 5
snd 6
""")
expected = {'snd': 6, 'rcv': 7}
assert actual == expected, actual


if __name__ == '__main__':
    import sys

    with open('input') as f:
        prog = f.read().strip()

    def rcv_triggered(snd):
        print(snd)
        sys.exit(0)

    interpreter(prog, rcv=rcv_triggered)

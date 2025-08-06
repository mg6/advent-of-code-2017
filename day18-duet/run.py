#!/usr/bin/env python3

from collections import defaultdict


class interpreter:
    """Parse and run a tablet program."""

    def __init__(self, prog, **kwargs):
        assert type(prog) is str

        self.prog = prog.strip().split("\n")
        self.regs = defaultdict[str, int](int)
        for k, v in kwargs.items():
            self.regs[k] = int(v)

        self.len = len(self.prog)
        self.pc = 0

    def get(self, name: str | int) -> int:
        """Return value of register or numeric literal."""
        try:
            return int(name)
        except ValueError:
            return self.regs[str(name)]

    def set(self, name: str, val: str | int):
        """Set register to the value of another register or numeric literal."""
        val = self.get(val)
        self.regs[name] = val

    def next(self):
        """True for program counter within bounds."""
        return 0 <= self.pc < self.len

    def run(self):
        """Run program until completion."""
        while self.next():
            self.step()
        return self.regs

    def until(self, cond):
        """Run program until condition is true."""
        while self.next():
            self.step()
            if cond(self):
                break
        return self.regs

    def cmd(self):
        """Get current command."""
        instr = self.prog[self.pc]
        cmd, *args = instr.split()
        return cmd, args

    def step(self):
        """Perform single program step."""
        cmd, args = self.cmd()

        if cmd == "set":
            reg, arg = args
            self.set(reg, arg)

        elif cmd == "add":
            reg, arg = args
            v = self.get(reg) + self.get(arg)
            self.set(reg, v)

        elif cmd == "mul":
            reg, arg = args
            v = self.get(reg) * self.get(arg)
            self.set(reg, v)

        elif cmd == "mod":
            reg, arg = args
            v = self.get(reg) % self.get(arg)
            self.set(reg, v)

        elif cmd == "jgz":
            reg, arg = args
            if self.get(reg) > 0:
                self.pc += self.get(arg)
                return

        elif cmd == "snd":
            arg, *_ = args
            self.set("snd", self.get(arg))

        elif cmd == "rcv":
            arg, *_ = args
            if self.get(arg) != 0:
                self.set("rcv", self.get("snd"))

        else:
            raise NotImplementedError

        self.pc += 1

    def snd(self):
        """Get played sound value."""
        return self.get("snd")

    def rcv(self):
        """Get recovered sound value."""
        return self.get("rcv")


if __name__ == "__main__":
    with open("input") as f:
        prog = f.read().strip()

    # part 1

    intp = interpreter(prog)
    regs = intp.until(lambda i: i.rcv() > 0)
    print(intp.rcv())

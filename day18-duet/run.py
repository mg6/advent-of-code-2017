#!/usr/bin/env python3

from collections import defaultdict, deque


class interpreter:
    """Parse and run a tablet program."""

    def __init__(self, prog, **kwargs):
        assert type(prog) is str

        self.prog = prog.strip().split("\n")
        self.regs = defaultdict[str, int](int)

        for k, v in kwargs.items():
            self.regs[k] = int(v)

        self.sendq = deque[int]()
        self.recvq = deque[int]()

        self.len = len(self.prog)
        self.pc = 0

        self.sendn = 0

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

    def run(self, cond=None):
        """Run program until completion or condition is true ."""
        while self.next():
            if not self.step():
                break
            if cond and cond(self):
                break
        return self.regs

    def cmd(self):
        """Get current command."""
        instr = self.prog[self.pc]
        cmd, *args = instr.split()
        return cmd, args

    def step(self) -> bool:
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
                return True

        elif cmd == "snd":
            arg, *_ = args
            v = self.get(arg)
            self.send(v)

        elif cmd == "rcv":
            arg, *_ = args
            try:
                if int(arg) != 0:
                    self.set("rcv", self.get("snd"))
            except ValueError:
                v, ok = self.recv()
                if not ok:
                    return False
                self.set(arg, v)

        else:
            raise NotImplementedError

        self.pc += 1
        return True

    def send(self, v: int):
        """Store value in output queue."""
        self.set("snd", v)
        self.sendq.append(v)
        self.sendn += 1

    def recv(self) -> tuple[int, bool]:
        """Receive value from input queue."""
        try:
            v = self.recvq.popleft()
            self.set("rcv", v)
            return v, True
        except IndexError:
            return 0, False

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

    p0 = interpreter(prog)
    regs = p0.run(lambda i: i.rcv() > 0)
    print(p0.snd())

    # part 2

    p1 = interpreter(prog, p=0)
    p2 = interpreter(prog, p=1)
    while True:
        while p2.sendq:
            p1.recvq.append(p2.sendq.popleft())

        done1 = p1.step()

        while p1.sendq:
            p2.recvq.append(p1.sendq.popleft())

        done2 = p2.step()

        if not done1 and not done2:
            # deadlock
            break

    print(p2.sendn)

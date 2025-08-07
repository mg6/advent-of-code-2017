from .run import interpreter


def test_set():
    prog = """
    set a 5
    """
    actual = interpreter(prog).run()
    expected = {"a": 5}
    assert actual == expected, actual

    prog = """
    set z 5
    """
    actual = interpreter(prog).run()
    expected = {"z": 5}
    assert actual == expected, actual


def test_set_many():
    prog = """
    set a 8
    set a 5
    """
    actual = interpreter(prog).run()
    expected = {"a": 5}
    assert actual == expected, actual


def test_add():
    prog = """
    add a 8
    """
    actual = interpreter(prog).run()
    expected = {"a": 8}
    assert actual == expected, actual


def test_mul():
    prog = """
    set a 8
    mul a 2
    """
    actual = interpreter(prog).run()
    expected = {"a": 16}
    assert actual == expected, actual


def test_mod():
    prog = """
    set a 8
    mod a 3
    """
    actual = interpreter(prog).run()
    expected = {"a": 2}
    assert actual == expected, actual


def test_jump_skip():
    prog = """
    add a 1
    jgz a 2
    add a 1
    """
    actual = interpreter(prog).run()
    expected = {"a": 1}
    assert actual == expected, actual


def test_jump():
    prog = """
    set a 8
    add a -1
    jgz a -1
    """
    actual = interpreter(prog).run()
    expected = {"a": 0}
    assert actual == expected, actual


def test_jump_empty():
    prog = """
    jgz 5 -1
    """
    actual = interpreter(prog).run()
    expected = {}
    assert actual == expected, actual


def test_snd():
    prog = """
    set a 8
    snd a
    """
    actual = interpreter(prog).run()
    expected = {"a": 8, "snd": 8}
    assert actual == expected, actual


def test_rcv_skip():
    prog = """
    snd 7
    rcv 0
    snd 6
    """
    actual = interpreter(prog).run()
    expected = {"snd": 6}
    assert actual == expected, actual


def test_rcv():
    prog = """
    snd 7
    rcv 5
    snd 6
    """
    actual = interpreter(prog).run()
    expected = {"snd": 6, "rcv": 7}
    assert actual == expected, actual


def test_send():
    prog = """
    snd 1
    snd 2
    snd p
    """
    intp = interpreter(prog, p=5)
    intp.run()
    assert list(intp.sendq) == [1, 2, 5]


def test_receive_none():
    prog = """
    rcv a
    rcv b
    rcv c
    rcv d
    """
    intp = interpreter(prog, p=5)
    assert intp.step() is False
    assert intp.pc == 0


def test_receive_some():
    prog = """
    rcv a
    rcv b
    rcv c
    rcv d
    """
    intp = interpreter(prog, p=5)
    intp.recvq.append(3)
    intp.recvq.append(2)
    intp.recvq.append(1)

    assert intp.step() is True
    assert intp.step() is True
    assert intp.step() is True
    assert intp.step() is False
    assert intp.pc == 3
    assert intp.step() is False
    assert intp.pc == 3
    assert intp.next()

    intp.recvq.append(7)

    assert intp.step() is True
    assert intp.pc == 4
    assert intp.rcv() == 7
    assert not intp.next()

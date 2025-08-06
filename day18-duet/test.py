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

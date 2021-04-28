from imports import *

def test_colors():
    x = Color(1, 2, 3)
    assert x.red == 1
    assert x.green == 2
    assert x.blue == 3


def test_add():
    assert Color(1, 2, 3)+Color(2, 3, 4) == Color(3, 5, 7)


def test_sub():
    assert Color(2, 3, 4)-Color(1, 2, 3) == Color(1, 1, 1)


def test_mul():
    assert Color(1, 2, 3) * 2 == Color(2, 4, 6)


def test_hadamard():
    assert Color(1, 2, 3).hadamard(Color(3, 4, 5)) == Color(3, 8, 15)


test_hadamard()

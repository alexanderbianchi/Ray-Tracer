from canvas import *


def test_colors_test():
    x = colors(1, 2, 3)

    assert x.red == 1
    assert x.green == 2
    assert x.blue == 3


def test_add_test():
    assert colors(1, 2, 3)+colors(2, 3, 4) == colors(3, 5, 7)


def test_sub_test():
    assert colors(2, 3, 4)-colors(1, 2, 3) == colors(1, 1, 1)


def test_mul_test():
    assert colors(1, 2, 3) * 2 == colors(2, 4, 6)


def test_hadamard_test():
    assert colors(1, 2, 3).hadamard(colors(3, 4, 5)) == colors(3, 8, 15)

from imports import *


def test_Point():
    p = Point(2, -2, 3)
    assert p.x == 2


def test_Vector():
    assert Vector(1, 2, 3) == Tuple(1, 2, 3, 0)


def test_add():
    assert Tuple(1, 2, 3, 0) + Tuple(1, 2, 3, 0) == Tuple(2, 4, 6, 0)


def test_sub():
    assert Tuple(2, 4, 6, 0) - Tuple(1, 2, 3, 0) == Tuple(1, 2, 3, 0)


def test_negate():
    a = Tuple(1, -2, 3, 0)
    print(a, -a)
    assert -a == Tuple(-1, 2, -3, 0)


def test_scalar():
    a = Tuple(1, -2, 3, -4)
    assert a * 3.5 == Tuple(3.5, -7, 10.5, -14)


def test_div():
    a = Tuple(1, -2, 3, -4)
    assert a / 2 == Tuple(.5, -1, 1.5, -2)


def test_frac():
    a = Tuple(1, -2, 3, -4)
    assert a * 0.5 == Tuple(.5, -1, 1.5, -2)


def test_magnitude():
    assert Vector(1, 0, 0).magnitude() == 1


def test_magnitude2():
    assert Vector(0, 1, 0).magnitude() == 1


def test_magnitude3():
    assert Vector(0, 1, 0).magnitude() == 1


def test_magnitude4():
    assert Vector(1, 2, 3).magnitude() == math.sqrt(14)


def test_magnitude5():
    assert Vector(-1, -2, -3).magnitude() == math.sqrt(14)


def test_dot():
    assert Vector(1, 2, 3).dot(Vector(2, 3, 4)) == 20


def test_normal():
    assert Vector(4, 0, 0).normalize() == Vector(1, 0, 0)


def test_normal1():
    assert Vector(1, 2, 3).normalize(), Vector(
        1/math.sqrt(14), 2/math.sqrt(14), 3/math.sqrt(14))


def test_cross():
    a = Vector(1, 2, 3)
    b = Vector(2, 3, 4)
    assert a.cross(b) == Vector(-1, 2, -1)
    assert b.cross(a) == Vector(1, -2, 1)

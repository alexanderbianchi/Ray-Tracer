from imports import *


def test_transformation():
    x = Translation(5, -3, 2)
    y = Vector(-3, 4, 5)
    z = Point(-3, 4, 5)
    print(x*z)
    assert x * y == y
    assert x * z == Tuple(2, 1, 7, 1)


def test_scaling():
    x = Scaling(2, 3, 4)
    y = Vector(-4, 6, 8)
    z = Point(-4, 6, 8)
    assert x*y == Vector(-8, 18, 32)
    assert x*z == Point(-8, 18, 32)
    inv = x.inverse()
    print(inv * y)
    assert inv * y == Vector(-2, 2, 2)
    tran = Scaling(-1, 1, 1)
    p = Point(2, 3, 4)
    assert tran * p == Point(-2, 3, 4)


test_scaling()


def test_x():

    p = Point(0, 1, 0)
    half_quarter = RotationX(pi / 4)
    full_quarter = RotationX(pi / 2)
    expected_half = Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    expected_full = Point(0, 0, 1)
    assert half_quarter * p == expected_half
    assert full_quarter * p == expected_full
    print(full_quarter * p)


def test_rotate_point_y():
    p = Point(0, 0, 1)
    half_quarter = RotationY(math.pi / 4)
    full_quarter = RotationY(math.pi / 2)
    expected_half = Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
    expected_full = Point(1, 0, 0)
    assert half_quarter * p == expected_half
    assert full_quarter * p == expected_full


def test_rotate_point_z():
    p = Point(0, 1, 0)
    half_quarter = RotationZ(math.pi / 4)
    full_quarter = RotationZ(math.pi / 2)
    expected_half = Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0)
    expected_full = Point(-1, 0, 0)
    assert half_quarter * p == expected_half
    assert full_quarter * p == expected_full


def test_shearing_x_to_y():
    transform = Shearing(1, 0, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    expected = Point(5, 3, 4)
    assert transform * p == expected


def test_shearing_x_to_z():
    transform = Shearing(0, 1, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    expected = Point(6, 3, 4)
    assert transform * p == expected


def test_shearing_y_to_x():
    transform = Shearing(0, 0, 1, 0, 0, 0)
    p = Point(2, 3, 4)
    expected = Point(2, 5, 4)
    assert transform * p == expected


def test_shearing_y_to_z():
    transform = Shearing(0, 0, 0, 1, 0, 0)
    p = Point(2, 3, 4)
    expected = Point(2, 7, 4)
    assert transform * p == expected


def test_shearing_z_to_x():
    transform = Shearing(0, 0, 0, 0, 1, 0)
    p = Point(2, 3, 4)
    expected = Point(2, 3, 6)
    assert transform * p == expected


def test_shearing_z_to_y():
    transform = Shearing(0, 0, 0, 0, 0, 1)
    p = Point(2, 3, 4)
    expected = Point(2, 3, 7)
    assert transform * p == expected


def test_transforms_in_sequence():
    p = Point(1, 0, 1)
    a = RotationX(math.pi / 2)
    b = Scaling(5, 5, 5)
    c = Translation(10, 5, 7)
    p2 = a * p
    assert p2 == Point(1, -1, 0)
    p3 = b * p2
    assert p3 == Point(5, -5, 0)
    p4 = c * p3
    assert p4 == Point(15, 0, 7)


def test_transforms_chained_reverse():
    p = Point(1, 0, 1)
    a = RotationX(math.pi / 2)
    b = Scaling(5, 5, 5)
    c = Translation(10, 5, 7)
    t = c * b * a
    assert t * p == Point(15, 0, 7)

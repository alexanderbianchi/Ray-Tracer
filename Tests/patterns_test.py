from imports import *

black = Color(0, 0, 0)
white = Color(1, 1, 1)


def test_create_stripe():
    p = Stripes(white, black)
    assert p.a == white and p.b == black


def test_constant_in_y():
    p = Stripes(white, black)

    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(0, 1, 0)) == white
    assert p.colorAt(Point(0, 2, 0)) == white


def test_constant_in_z():
    p = Stripes(white, black)

    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(0, 0, 1)) == white
    assert p.colorAt(Point(0, 0, 1)) == white


def test_constant_in_x():
    p = Stripes(white, black)

    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(.9, 0, 0)) == white
    assert p.colorAt(Point(1, 0, 0)) == black
    assert p.colorAt(Point(-.1, 0, 0)) == black
    assert p.colorAt(Point(-1, 0, 0)) == black
    assert p.colorAt(Point(-1.1, 0, 0)) == white


def test_lighting_with_pattern():
    m = Material()
    m.pattern = Stripes(white, black)
    m.ambient = 1
    m.diffuse = 0
    m.specular = 0
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    s = Sphere()
    light = PointLight(Point(0, 0, -10), white)
    c1 = lighting(m, light, Point(0.9, 0, 0), eyev, normalv, False, s)
    c2 = lighting(m, light, Point(1.1, 0, 0), eyev, normalv, False, s)
    assert c1 == white
    assert c2 == black


def test_stripes_object_transformation():
    obj = Sphere()
    obj.set_transform(Scaling(2, 2, 2))
    p = TestPattern(white, black)
    c = p.colorAtObject(Point(2, 3, 4), obj)
    assert c == Color(1, 1.5, 2)


def test_stripes_pattern_transformation():
    obj = Sphere()

    p = TestPattern(white, black)
    p.setTransform(Scaling(2, 2, 2))
    c = p.colorAtObject(Point(2, 3, 4), obj)

    assert c == Color(1, 1.5, 2)


def test_stripes_both_transformation():
    obj = Sphere()
    obj.set_transform(Scaling(2, 2, 2))
    p = TestPattern(white, black)
    p.setTransform(Translation(0.5, 1, 1.5))
    c = p.colorAtObject(Point(2.5, 3, 3.5), obj)
    print(c)
    assert c == Color(0.75, 0.5, 0.25)


def test_default_pattern():
    p = Pattern(white, black)
    assert p.transform == Matrix([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])


def test_default_pattern_transform():
    p = Pattern(white, black)
    p.setTransform(Translation(1, 2, 3))
    assert p.transform == Translation(1, 2, 3)


def test_gradient():
    p = Gradient(white, black)
    assert p.colorAt(Point(0.25, 0, 0)) == Color(0.75, 0.75, 0.75)
    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(0.5, 0, 0)) == Color(0.5, 0.5, 0.5)
    assert p.colorAt(Point(0.75, 0, 0)) == Color(0.25, 0.25, 0.25)


def test_ring():
    p = Rings(white, black)
    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(1, 0, 0)) == black
    assert p.colorAt(Point(0, 0, 1)) == black
    assert p.colorAt(Point(0.708, 0, 0.708)) == black


def test_checkers():
    p = Checkers(white, black)
    assert p.colorAt(Point(0, 0, 0)) == white
    assert p.colorAt(Point(.99, 0, 0)) == white
    assert p.colorAt(Point(1.01, 0, 0)) == black

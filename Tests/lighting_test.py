from imports import *


def test_normalX():
    s = Sphere()
    n = s.normalize_at(Point(1, 0, 0))
    print(n)
    assert n == Vector(1, 0, 0)


test_normalX()


def test_normalY():
    s = Sphere()
    n = s.normalize_at(Point(0, 1, 0))
    assert n == Vector(0, 1, 0)


def test_normalZ():
    s = Sphere()
    n = s.normalize_at(Point(0, 0, 1))
    assert n == Vector(0, 0, 1)


def test_normalZ():
    s = Sphere()
    var = (math.sqrt(3)/3)
    n = s.normalize_at(Point(var, var, var))
    assert n == Vector(var, var, var)


def test_normal_translated():
    s = Sphere()
    s.set_transform(Translation(0, 1, 0))
    n = s.normalize_at(Point(0, 1.70711, -0.70711))

    assert n == Vector(0, 0.70711, -0.70711)


def test_normal_translated_2():
    s = Sphere()
    m = Scaling(1, 0.5, 1) * RotationZ(math.pi / 5)
    s.set_transform(m)
    n = s.normalize_at(Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2))
    print(n)
    assert n == Vector(0, 0.97014, -0.24254)


def test_45_reflect():
    v = Vector(1, -1, 0)
    n = Vector(0, 1, 0)
    r = v.reflect(n)
    assert r == Vector(1, 1, 0)


def test_other_reflect():
    v = Vector(0, -1, 0)
    n = Vector(math.sqrt(2) / 2,  math.sqrt(2) / 2, 0)
    r = v.reflect(n)
    assert r == Vector(1, 0, 0)


def test_light():
    light = PointLight(Point(0, 0, 0), Color(1, 1, 1))
    assert light.position == Point(
        0, 0, 0) and light.intensity == Color(1, 1, 1)


def test_material():
    m = Material()
    assert m.color == Color(1, 1, 1)
    assert m.ambient == 0.1
    assert m.specular == 0.9


def test_default_material():
    s = Sphere()
    assert s.material == Material()


def test_assign_material():
    s = Sphere()
    m = Material()
    m.color = Color(0, 0, 0)
    s.material = m
    assert s.material == m


def test_lighting():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.9, 1.9, 1.9)


def test_lighting2():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.0, 1.0, 1.0)


def test_lighting3():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.7364, 0.7364, 0.7364)


def test_lighting4():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.6364, 1.6364, 1.6364)


def test_lighting5():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.1, 0.1, 0.1)


def test_lighting6():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.1, 0.1, 0.1)

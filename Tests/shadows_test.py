from imports import *


def test_lighting_with_surface_in_shadow():
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    inShadow = True
    m = Material()
    result = lighting(m, light, Point(0, 0, 0), eyev, normalv, inShadow)
    print(result)
    assert result == Color(0.1, 0.1, 0.1)


def test_no_shadow():
    w = World()
    p = Point(0, 10, 0)
    assert w.isShadowed(p) is False


def test_shadow_behind_camera():
    w = World()
    p = Point(-20, 20, -20)
    assert w.isShadowed(p) is False


def test_shadow_bewteen_point_light():
    w = World()
    p = Point(10, -10, 10)
    assert w.isShadowed(p) is True


def test_shadow_behind_point():
    w = World()
    p = Point(-2, 2, -2)
    assert w.isShadowed(p) is False


test_shadow_behind_point()


def test_shadeHit_given_in_shadow():
    w = World()
    w.light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    s1 = Sphere()
    s2 = Sphere()
    s2.set_transform(Translation(0, 0, 10))
    objs = s1, s2
    w.objects = objs
    r = Ray(Point(0, 0, 1), Vector(0, 0, 1))
    i = Intersection(4, s2)
    comps = i.prep(r)
    c = w.shadeHit(comps, 5)
    print(comps['overPoint'], comps['point'])
    assert c == Color(0.1, 0.1, 0.1)


EPSILON = 0.00001


def test_offset_hit():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.set_transform(Translation(0, 0, 1))
    i = Intersection(5, shape)
    comps = i.prep(r)
    print(comps['overPoint'].z)
    assert comps['overPoint'].z < -EPSILON/2
    assert comps['point'].z > comps['overPoint'].z

from imports import *


def test_default_transformation():
    s = Shape()
    assert s.transform == Matrix([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])


def test_assign_transformation():
    s = Shape()
    s.set_transform(Translation(2, 3, 4))
    assert s.transform == Translation(2, 3, 4)


def test_default_material():
    s = Shape()
    m = s.material
    assert m == Material()


def test_assigning_material():
    s = Shape()
    m = Material()
    m.ambient = 1
    s.material = m
    assert s.material.ambient == 1


def test_intersecting_scaled_ray():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = TestShape()
    s.set_transform(Scaling(2, 2, 2))
    xs = r.intersect(s)
    assert s.savedRay.origin == Point(0, 0, -2.5)
    assert s.savedRay.direction == Vector(0, 0, 0.5)


def test_intersecting_translated_ray():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = TestShape()
    s.set_transform(Translation(5, 0, 0))
    xs = r.intersect(s)
    assert s.savedRay.origin == Point(-5, 0, -5)
    assert s.savedRay.direction == Vector(0, 0, 1)


def test_normal_translated_shape():
    s = TestShape()
    s.set_transform(Translation(0, 1, 0))
    n = s.normalize_at(Point(0, 1.70711, -0.70711))
    assert n == Vector(0, 0.70711, -0.70711)


def test_normal_transformed_shape():
    s = TestShape()
    s.set_transform(Scaling(1, 0.5, 1)*RotationZ(math.pi/5))
    n = s.normalize_at(Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))

    assert n == Vector(0, 0.97014, -0.24254)


def test_normal_plane():
    p = Plane()
    n1 = p.localNormalAt()
    assert n1 == Vector(0, 1, 0)


def test_parallel_intersec_plane():
    p = Plane()
    r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
    xs = p.localIntersect(r)
    assert xs == False


def test_intersect_with_coplanar():
    p = Plane()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = p.localIntersect(r)
    assert xs is False


def test_intersect_from_above():
    p = Plane()
    r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
    xs = p.localIntersect(r)
    assert (len(xs) == 1)
    assert (xs[0].t == 1)
    assert (xs[0].obj == p)


def test_intersect_from_below():
    p = Plane()
    r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
    xs = p.localIntersect(r)
    assert (len(xs) == 1)
    assert (xs[0].t == 1)
    assert (xs[0].obj == p)


test_intersect_from_below()

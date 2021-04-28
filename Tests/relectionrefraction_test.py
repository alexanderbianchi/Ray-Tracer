from imports import *


def test_material_reflectiviy():
    m = Material()
    assert m.reflectivity == 0


def test_precompute_refletivity():
    s = Plane()
    r = Ray(Point(0, 1, -1), Vector(0, -math.sqrt(2) /
                                    math.sqrt(2), math.sqrt(2)/math.sqrt(2)))
    i = Intersection(math.sqrt(2), s)
    comps = i.prep(r)
    assert comps['reflectv'] == Vector(0, math.sqrt(
        2)/math.sqrt(2), math.sqrt(2)/math.sqrt(2))


def test_reflect_nonreflective():
    w = World()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    s = w.objects[1]
    s.material.ambient = 1
    i = Intersection(1, s)
    comps = i.prep(r)
    color = w.reflectiveColor(comps, 5)
    assert color == Color(0, 0, 0)


def test_hit_reflective():
    w = World()
    s = Plane()
    s.material.reflectivity = 0.5
    s.transform = (Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) /
                                    2, math.sqrt(2)/2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prep(r)
    color = w.reflectiveColor(comps, 5)
    assert color == Color(0.19032, 0.2379, 0.14274)


def test_update_shadehit():
    w = World()
    s = Plane()
    s.material.reflectivity = 0.5
    s.transform = (Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) /
                                    2, math.sqrt(2)/2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prep(r)
    color = w.shadeHit(comps, 5)
    assert color == Color(0.87677, 0.92436, 0.82918)


def test_infinite_recursion():
    w = World()
    w.light = PointLight(Point(0, 0, 0), Color(1, 1, 1))
    lower = Plane()
    lower.material.reflectivity = 1
    lower.set_transform(Translation(0, -1, 0))
    upper = Plane()
    upper.material.reflectivity = 1
    upper.set_transform(Translation(0, 1, 0))
    w.objects == lower, upper
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    assert w.colorAt(r, 10)


def test_limit_recursion():
    w = World()
    s = Plane()
    s.material.reflectivity = 0.5
    s.transform = (Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) /
                                    2, math.sqrt(2)/2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prep(r)
    color = w.reflectiveColor(comps, 0)
    assert color == Color(0, 0, 0)

## Refraction ##


def GlassSphere():
    s = Sphere()
    s.material.refractiveIndex = 1.5
    s.material.transparency = 1
    return s


def test_default_material_reflective():
    m = Material()
    assert m.transparency == 0
    assert m.refractiveIndex == 1


def test_default_glass_sphere():
    s = GlassSphere()
    assert s.transform == Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                                  [0, 0, 1, 0], [0, 0, 0, 1]])
    assert s.material.transparency == 1
    assert s.material.refractiveIndex == 1.5


def test_find_n1_n2():
    a = GlassSphere()
    a.set_transform(Scaling(1, 1, 1))
    a.material.refractiveIndex = 1.5
    b = GlassSphere()
    b.set_transform(Translation(0, 0, -0.25))
    b.material.refractiveIndex = 2
    c = GlassSphere()
    c.set_transform(Translation(0, 0, 0.25))
    c.material.refractiveIndex = 2.5
    r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
    ints = [Intersection(2, a), Intersection(2.75, b), Intersection(3.25, c),
            Intersection(4.75, b), Intersection(5.25, c), Intersection(6, a)]
    examples = {0: [1, 1.5], 1: [1.5, 2], 2: [2.0, 2.5],
                3: [2.5, 2.5], 4: [2.5, 1.5], 5: [1.5, 1.0]}
    xs = Intersections(*ints)

    for i in range(len(ints)):
        comps = ints[i].prep(r, xs)
        assert comps['n1'] == examples[i][0]
        assert comps['n2'] == examples[i][1]


def test_underpoint():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = GlassSphere()
    s.set_transform(Translation(0, 0, 1))
    i = Intersection(5, s)
    xs = Intersections(i)
    comps = i.prep(r, xs)
    assert comps['underPoint'].z > 0.001 / 2
    assert comps["point"].z < comps['underPoint'].z


def test_refracted_opaque():
    w = World()
    s = w.objects[0]
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, s), Intersection(6, s))
    comps = xs[0].prep(r, xs)
    c = w.refracted(comps, 5)
    assert c == Color(0, 0, 0)


def test_limit_recursion_refractivity():
    w = World()
    s = w.objects[0]
    s.material.transparency = 1
    s.material.refractiveIndex = 1.5
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, s), Intersection(6, s))
    comps = xs[0].prep(r, xs)
    c = w.refracted(comps, 0)
    assert c == Color(0, 0, 0)


def test_internal_reflection_metal_band():
    w = World()
    s = w.objects[0]
    s.material.transparency = 1
    s.material.refractiveIndex = 1.5
    r = Ray(Point(0, 0, -math.sqrt(2)/2), Vector(0, 1, 0))
    xs = Intersections(Intersection(-math.sqrt(2)/2, s),
                       Intersection(math.sqrt(2)/2, s))
    comps = xs[1].prep(r, xs)
    c = w.refracted(comps, 5)
    assert c == Color(0, 0, 0)


def test_recracted_color():  # NOT WORKING
    w = World()
    a = w.objects[0]
    a.material.ambient = 1
    a.pattern = TestPattern(Color(1, 1, 1), Color(0, 0, 0))
    b = w.objects[1]
    b.material.transparency = 1
    b.material.refractiveIndex = 1.5
    r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
    xs = Intersections(Intersection(-0.9899, a),
                       Intersection(-0.4899, b), Intersection(0.4899,
                                                              b), Intersection(0.9899, a))
    comps = xs[2].prep(r, xs)
    c = w.refracted(comps, 5)
    print(c)
    assert c == Color(0, 0.99888, 0.04725)


def test_refraction_shade_hit():
    w = World()
    f = Plane()
    f.set_transform(Translation(0, -1, 0))
    f.material.transparency = 0.5
    f.material.refractiveIndex = 1.5
    w.objects.append(f)
    s = Sphere()
    s.material.color = Color(1, 0, 0)
    s.material.ambient = 0.5
    s.set_transform(Translation(0, -3.5, -0.5))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    xs = Intersections(Intersection(math.sqrt(2), f))
    comps = xs[0].prep(r, xs)
    color = w.shadeHit(comps, 5)
    print(color)
    assert color == Color(0.93642, 0.68642, 0.68642)


def test_schlick_total_reflection():
    s = GlassSphere()
    r = Ray(Point(0, 0, math.sqrt(2)), Vector(0, 1, 0))
    xs = Intersections(Intersection(-math.sqrt(2)/2, s),
                       Intersection(math.sqrt(2)/2, s))
    comps = xs[1].prep(r, xs)
    reflectance = schlick(comps)
    assert reflectance == 1


def compare(a, b):
    EPSILON = 0.0001
    if abs(a-b) < EPSILON:
        return True
    else:
        return False


def test_schlick_perpendicular_reflection():
    s = GlassSphere()
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    xs = Intersections(Intersection(-1, s),
                       Intersection(1, s))
    comps = xs[1].prep(r, xs)
    reflectance = schlick(comps)
    assert compare(reflectance, 0.04)


def test_schlick_smallangle_reflection():
    s = GlassSphere()
    r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
    xs = Intersections(Intersection(1.8589, s))
    comps = xs[0].prep(r, xs)
    reflectance = schlick(comps)
    print(reflectance)
    assert compare(reflectance, 0.48873)


def test_refraction_shade_hit():
    w = World()
    f = Plane()
    f.set_transform(Translation(0, -1, 0))
    f.material.transparency = 0.5
    f.material.refractiveIndex = 1.5
    F.material.reflectivity = 0.5
    w.objects.append(f)
    s = Sphere()
    s.material.color = Color(1, 0, 0)
    s.material.ambient = 0.5
    s.set_transform(Translation(0, -3.5, -0.5))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    xs = Intersections(Intersection(math.sqrt(2), f))
    comps = xs[0].prep(r, xs)
    color = w.shadeHit(comps, 5)
    assert color == Color(0.93391, 0.69643, 0.69243)

from imports import *


def test_world():
    w = World()
    assert len(w.objects) == 2
    assert w.light


def test_default_world():
    x = Sphere()
    y = Sphere()
    x.material = Material(Color(.8, 1, .6), 0.1, 0.7, 0.9, 200)
    y.transform *= Scaling(0.5, 0.5, 0.5)
    w = World()
    assert w.objects[0] == x
    assert w.objects[1] == y
    assert w.light == PointLight(Point(-10, 10, -10), Color(1, 1, 1))


def test_intersect_world_ray():
    w = World()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = w.intersect(r)

    assert xs[0] == 4


def test_computation_prep():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prep(r)
    assert comps['point'] == Point(0, 0, -1)
    assert comps['eyev'] == Vector(0, 0, -1)
    assert comps['object'] == i.obj
    assert comps['normalv'] == Vector(0, 0, -1)


def test_inside_false():
    w = World()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = w.objects[0]
    i = Intersection(4, shape)
    comps = i.prep(r)
    assert comps['inside'] == False


def test_inside_true():
    w = World()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prep(r)
    assert comps['inside'] == True
    assert comps['point'] == Point(0, 0, 1)
    assert comps['eyev'] == Vector(0, 0, -1)
    assert comps['normalv'] == Vector(0, 0, -1)


def test_shading_intersection():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    w = World()
    shape = w.objects[0]
    i = Intersection(4, shape)
    comps = i.prep(r)
    c = w.shadeHit(comps, 5)
    assert c == Color(0.38066, 0.47583, 0.2855)


def test_shading_intersection_inside():
    w = World()
    w.light = PointLight(Point(0, 0.25, 0), Color(1, 1, 1))
    shape = w.objects[1]
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    i = Intersection(.5, shape)
    comps = i.prep(r)
    c = w.shadeHit(comps, 5)
    assert c == Color(0.90498, 0.90498, 0.90498)


def test_ray_misses():
    w = World()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    c = w.colorAt(r, 5)
    assert c == Color(0, 0, 0)


def test_ray_hits():
    w = World()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    c = w.colorAt(r, 5)
    assert c == Color(0.38066, 0.47583, 0.2855)


def test_intersection_behind_ray():
    w = World()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, .75), Vector(0, 0, -1))
    c = w.colorAt(r, 5)
    assert c == inner.material.color


def test_default_transformation():
    f = Point(0, 0, 0)
    to = Point(0, 0, -1)
    up = Vector(0, 1, 0)
    t = viewTransform(f, to, up)
    assert t == Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                        [0, 0, 1, 0], [0, 0, 0, 1]])


def test_view_transformation_matrix_in_positive_z_direction():
    f = Point(0, 0, 0)
    to = Point(0, 0, 1)
    up = Vector(0, 1, 0)
    t = viewTransform(f, to, up)
    assert t == Scaling(-1, 1, -1)


def test_view_transform_moves_the_world():
    f = Point(0, 0, 8)
    to = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    t = viewTransform(f, to, up)
    assert t == Translation(0, 0, -8)


def test_arbitrary_view_transformation():
    frm = Point(1, 3, 2)
    to = Point(4, -2, 8)
    up = Vector(1, 1, 0)
    t = viewTransform(frm, to, up)
    assert t == Matrix([
        [-0.50709, 0.50709, 0.67612, -2.36643],
        [0.76772, 0.60609, 0.12122, -2.82843],
        [-0.35857, 0.59761, -0.71714, 0.00000],
        [0.00000, 0.00000, 0.00000, 1.00000],
    ])


def test_camera_construction():
    hsize = 160
    vsize = 120
    fov = math.pi / 2
    c = Camera(hsize, vsize, fov)
    assert (c.hsize == 160)
    assert (c.vsize == 120)
    assert (c.fov == math.pi / 2)
    assert (c.transform == Matrix([[1, 0, 0, 0], [
        0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))


def test_horizontal_pixel_size():
    c = Camera(200, 125, math.pi / 2)
    assert abs(c.pixelSize - 0.01) < 0.00001


def test_vertical_pixel_size():
    c = Camera(125, 200, math.pi / 2)
    assert abs(c.pixelSize - 0.01) < 0.00001


def test_ray_through_center_of_canvas():
    c = Camera(201, 101, math.pi / 2)
    r = c.rayForPixel(100, 50)
    print(r.direction)
    assert (r.origin == Point(0, 0, 0))
    assert (r.direction == Vector(0, 0, -1))


def test_ray_through_corner_of_canvas():
    c = Camera(201, 101, math.pi / 2)
    r = c.rayForPixel(0, 0)
    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector(0.66519, 0.33259, -0.66851)


def test_ray_when_camera_is_transformed():
    transform = RotationY(math.pi / 4) * Translation(0, -2, 5)
    c = Camera(201, 101, math.pi / 2, transform)
    r = c.rayForPixel(100, 50)
    assert (r.origin == Point(0, 2, -5))
    assert (r.direction == Vector(math.sqrt(2) / 2, 0, -math.sqrt(2) / 2))


# def test_world_with_camera():
#     w = World()
#     frm = Point(0, 0, -5)
#     to = Point(0, 0, 0)
#     up = Vector(0, 1, 0)
#     c = Camera(11, 11, math.pi/2)
#     c.transform = viewTransform(frm, to, up)
#     image = c.render(w)
#     assert image.pixel_at(5, 5) == Color(0.38066, 0.47583, 0.2855)

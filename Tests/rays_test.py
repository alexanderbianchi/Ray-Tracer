from imports import *

def test_creation():
    o = Point(1, 2, 3)
    d = Vector(4, 5, 6)
    r = Ray(o, d)
    assert r.origin == o
    assert r.direction == d


def test_position():
    r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
    assert r.position(0) == Point(2, 3, 4)
    assert r.position(1) == Point(3, 3, 4)
    assert r.position(-1) == Point(1, 3, 4)
    assert r.position(2.5) == Point(4.5, 3, 4)


def test_intersection():
    s = Sphere()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i[0] == 4 and i[1] == 6


def test_intersection_tangent():
    s = Sphere()
    r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i[0] == 5 and i[1] == 5


def test_intersection_misses():
    s = Sphere()
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i == False


def test_intersection_inside():
    s = Sphere()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i[0] == -1 and i[1] == 1


def test_intersection_infront():
    s = Sphere()
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i[0] == -6 and i[1] == -4


def test_intersection_class():
    s = Sphere()
    i = Intersection(3.5, s)
    assert i.t == 3.5 and i.obj == s


def test_intersection_obj():
    s = Sphere()
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    i = r.intersect(s)
    assert i[0].obj == s and i[1].obj == s


def test_intersections():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i1, i2)
    assert xs[0] == 1


def test_hit():
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    i5 = Intersections(i1, i2, i3, i4).hit()
    print(i5)
    assert i5 == i4


def test_translate_ray():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Translation(3, 4, 5)
    r2 = r.transform(m)
    assert r2.origin == Point(4, 6, 8)
    assert r2.direction == Vector(0, 1, 0)


def test_scale_ray():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == Point(2, 6, 12)
    assert r2.direction == Vector(0, 3, 0)


def test_identity():
    s = Sphere()
    assert s.transform == Matrix([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])


def test_set_transform():
    s = Sphere()
    s.set_transform(Translation(2, 3, 4))
    assert s.transform == Translation(2, 3, 4)


def test_intersect_transform():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    s.set_transform(Scaling(2, 2, 2))
    xs = r.intersect(s)
    assert xs[0] == 3
    assert xs[1] == 7


# canvas_pixels = 500
# view = Canvas(canvas_pixels, canvas_pixels)
# shape = Sphere()
# shape.material.color = colors(1, 0.2, 1)
# light_position = Point(-10, 10, -10)
# light_color = colors(1, 1, 1)
# light = point_light(light_position, light_color)

# wall_size = 7
# pixel_size = wall_size/canvas_pixels
# half = wall_size/2
# origin = Point(0, 0, -5)
# wall_z = 10


# for y in range(view.height-1):
#     world_y = half - (pixel_size*y)
#     for x in range(view.width-1):
#         world_x = -half + (pixel_size*x)
#         position = Point(world_x, world_y, wall_z)
#         temp = position - origin
#         r = Ray(origin, temp.normalize())
#         xs = r.intersect(shape)
#         if xs != False:
#             hit = xs.hit()
#             if hit:
#                 point = r.position(hit.t)
#                 normal = hit.obj.normalize_at(point)
#                 eye = -r.direction
#                 color = lighting(hit.obj.material, light, point, eye, normal)
#                 view.write_pixel(x, y, color)


# view.convert_to_ppm('Wabbajack.ppm')

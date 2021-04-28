from raytracer.components.tuples import *
from raytracer.components.matrix import *
import math
from raytracer.components.rays import *
from raytracer.components.canvas import *
from raytracer.components.lighting import *


class Shape():
    def __init__(self):

        self.transform = Matrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])
        self.material = Material()

    def set_transform(self, transform):
        self.transform = transform*self.transform

    def normalize_at(self, point):
        invtran = self.transform.inverse()
        object_point = invtran * point
        object_normal = self.localNormalAt(object_point)
        world_normal = invtran.transpose() * object_normal
        world_normal.w = 0
        return world_normal.normalize()


class Sphere(Shape):
    def __init__(self):
        super().__init__()
        self.radius = 1
        self.center = Point(0, 0, 0)

    def localNormalAt(self, object_point):
        return object_point - self.center

    def __eq__(self, other):
        try:
            if self.center == other.center and self.radius == other.radius and self.transform == other.transform and self.material == other.material:
                return True
        except:
            pass
        return False

    def localIntersect(self, ray2):
        to_ray = ray2.origin - self.center
        a = ray2.direction.dot(ray2.direction)
        b = 2 * ray2.direction.dot(to_ray)
        c = to_ray.dot(to_ray) - self.radius
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return False
        t1 = (-b - math.sqrt(discriminant)) / (2*a)
        t2 = (-b + math.sqrt(discriminant)) / (2*a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))


class Plane(Shape):
    def __init__(self):
        super().__init__()

    def localIntersect(self, ray):
        if abs(ray.direction.y) < 0.0001:
            return False
        t = - ray.origin.y/ray.direction.y
        return Intersections(Intersection(t, self))

    def localNormalAt(self, object_point=False):
        return Vector(0, 1, 0)


class TestShape(Shape):
    def __init__(self):
        super().__init__()

    def localIntersect(self, ray):
        self.savedRay = ray

    def localNormalAt(self, object_point):
        return Vector(object_point.x, object_point.y, object_point.z)


class Intersections():
    def __init__(self, *args):
        self.intersections = [i for i in args]
        self.intersections.sort()

    def __str__(self):
        return str(str(x) for x in self.intersections)

    def __getitem__(self, num):
        return self.intersections[num]

    def add(self, i):
        self.intersections.append(i)
        self.intersections.sort()
        # sorting every time into an already sorted array is inneficient
        # to be refactored in C implimentation

    def count(self):
        return len(self.intersections)

    def hit(self):
        if self.intersections:
            for i in self.intersections:

                if i.t > 0:
                    return i
        return False

    def __len__(self):
        return len(self.intersections)


class Intersection():
    def __init__(self, t, obj):
        self.t = t  # t == ray
        self.obj = obj

    def __str__(self):
        return str(self.t)

    def prep(self, r,  xs=False):
        comps = {}
        comps['t'] = self.t
        comps['object'] = self.obj
        comps['point'] = r.position(comps['t'])
        comps['eyev'] = -r.direction
        comps['normalv'] = comps['object'].normalize_at(comps['point'])
        if comps['normalv'].dot(comps['eyev']) < 0:
            comps['inside'] = True
            comps["normalv"] = -comps['normalv']
        else:
            comps['inside'] = False
        comps['overPoint'] = comps['point'] + comps['normalv'] * 0.001
        comps['underPoint'] = comps['point'] - comps['normalv'] * 0.001
        comps['reflectv'] = r.direction.reflect(comps['normalv'])
        if xs:
            hit = self
            containers = []
            objects = set()
            for i in xs.intersections:

                if i.t == hit.t and i.obj == hit.obj:

                    if len(containers) == 0:
                        comps['n1'] = 1
                    else:
                        comps['n1'] = containers[-1].obj.material.refractiveIndex

                if id(i) in objects:
                    objects.remove(id(i))
                    j = 0
                    while True:
                        if containers[j] == i:
                            del containers[j]
                            break
                        j += 1

                else:
                    containers.append(i)
                    objects.add(id(i))

                if i.t == hit.t and i.obj == hit.obj:

                    if len(containers) == 0:
                        comps['n2'] = 1
                    else:
                        comps['n2'] = containers[-1].obj.material.refractiveIndex

        return comps

    def __eq__(self, other):
        if self.t == other or self.t == other.t:
            return True
        return False

    def __lt__(self, other):
        return self.t < other.t

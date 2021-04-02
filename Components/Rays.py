from chapter1 import *
from Matrice import *
from transformations import *
import math
from Lighting import *


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + (self.direction * t)

    def intersect(self, obj):
        ray2 = self.transform(obj.transform.inverse())
        to_ray = ray2.origin - obj.center
        a = ray2.direction.dot(ray2.direction)
        b = 2 * ray2.direction.dot(to_ray)
        c = to_ray.dot(to_ray) - obj.radius
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return False
        t1 = (-b - math.sqrt(discriminant)) / (2*a)
        t2 = (-b + math.sqrt(discriminant)) / (2*a)
        return intersections(intersection(t1, obj), intersection(t2, obj))

    def transform(self, matrix):
        return Ray(matrix * self.origin, matrix * self.direction)


class intersections():
    def __init__(self, *args):
        self.intersections = [i for i in args]
        self.intersections.sort()

    def __getitem__(self, num):
        return self.intersections[num]

    def count(self):
        return len(self.intersections)

    def hit(self):
        if self.intersections:
            for i in self.intersections:
                if i.t > 0:
                    return i


class intersection():
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj

    def __str__(self):
        return str(self.t)

    def __eq__(self, other):
        if self.t == other:
            return True
        return False

    def __lt__(self, other):
        return self.t < other.t


class Sphere():
    def __init__(self):
        self.center = Point(0, 0, 0)
        self.radius = 1
        self.transform = matrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])
        self.material = material()

    def set_transform(self, transform):
        self.transform = transform*self.transform

    def normalize_at(self, point):
        invtran = self.transform.inverse()
        object_point = invtran * point
        object_normal = object_point - Point(0, 0, 0)
        world_normal = invtran.transpose() * object_normal
        world_normal.w = 0
        return world_normal.normalize()

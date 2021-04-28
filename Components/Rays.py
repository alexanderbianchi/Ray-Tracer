from raytracer.components.lighting import *
from raytracer.components.tuples import *
from raytracer.components.matrix import *
import math
from raytracer.components.canvas import *


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + (self.direction * t)

    def intersect(self, obj):
        ray2 = self.transform(obj.transform.inverse())
        return obj.localIntersect(ray2)

    def transform(self, matrix):
        return Ray(matrix * self.origin, matrix * self.direction)

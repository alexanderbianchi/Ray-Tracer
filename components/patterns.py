from raytracer.components.tuples import *
from raytracer.components.matrix import *
import math


class Pattern():
    def __init__(self, colorA, colorB):
        self.a = colorA
        self.b = colorB
        self.transform = Matrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

    def colorAt(self, point):
        return self.localColorAt(point)

    def colorAtObject(self, point, obj):
        objectPoint = obj.transform.inverse() * point
        patternPoint = self.transform.inverse() * objectPoint
        return self.localColorAt(patternPoint)

    def setTransform(self, transform):
        self.transform = transform*self.transform


class Stripes(Pattern):
    def __init__(self, colorA, colorB):
        super().__init__(colorA, colorB)

    def localColorAt(self, point):
        if math.floor(point.x) % 2 == 0:
            return self.a

        else:
            return self.b


class TestPattern(Pattern):
    def __init__(self, colorA, colorB):
        super().__init__(colorA, colorB)

    def localColorAt(self, p):
        return Color(p.x, p.y, p.z)


class Gradient(Pattern):
    def __init__(self, colorA, colorB):
        super().__init__(colorA, colorB)

    def localColorAt(self, p):
        distance = self.b - self.a
        fraction = p.x - math.floor(p.x)
        return self.a + ((distance) * (fraction))


class Rings(Pattern):
    def __init__(self, colorA, colorB):
        super().__init__(colorA, colorB)

    def localColorAt(self, p):

        if math.floor(math.sqrt((p.x * p.x) + (p.z * p.z))) % 2 == 0:

            return self.a

        else:
            return self.b


class Checkers(Pattern):
    def __init__(self, colorA, colorB):
        super().__init__(colorA, colorB)

    def localColorAt(self, p):
        if (math.floor(p.x) + math.floor(p.y) + math.floor(p.z)) % 2 == 0:
            return self.a
        else:
            return self.b

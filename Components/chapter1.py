import math


def compare(a, b):
    EPSILON = 0.001
    if abs(a-b) < EPSILON:
        return True
    else:
        return False


class Tuple():
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __getitem__(self, y):
        if y == 0:
            return self.x
        if y == 1:
            return self.y
        if y == 2:
            return self.z
        if y == 3:
            return self.w

    def isVector(self):
        return False if w == 0 else True

    def isPoint(self):
        return False if w == 1 else True

    def isTuple(self):
        return True

    def __eq__(self, other):
        if (not compare(self.x, other.x) or  # !compare(self.x,other.x) or
            not compare(self.y, other.y) or  # not compare(self.y,other.y) or
            not compare(self.z, other.z) or  # not compare(self.z,other.z) or
                not compare(self.w, other.w)):  # not compare(self.w,other.w)
            return False

        else:
            return True

    def __str__(self):
        return str(self.show())

    def show(self):
        return (self.x, self.y, self.z, self.w)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        w = self.w + other.w

        return Tuple(x, y, z, w)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        w = self.w - other.w

        return Tuple(x, y, z, w)

    def __neg__(self):
        x = -self.x
        y = -self.y
        z = -self.z
        return Tuple(x, y, z, self.w)

    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        z = self.z * scalar
        w = self.w * scalar
        return Tuple(x, y, z, w)

    def __truediv__(self, div):
        self.x /= div
        self.y /= div
        self.z /= div
        self.w /= div
        return self

    def dot(self, other):
        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z +
            self.w * other.w
        )

    def magnitude(self):
        return math.sqrt(
            self.x**2 +
            self.y**2 +
            self.z**2 +
            self.w**2
        )

    def normalize(self):
        magnitude = self.magnitude()
        self.x = self.x/magnitude
        self.y = self.y/magnitude
        self.z = self.z/magnitude
        self.w = self.w/magnitude
        return self

    def transformation(self, x, y, z):
        identity = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        self.matrix = self.matrix * matrix(identity)

    def scaling(self, x, y, z):
        identity = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
        self.matrix = self.matrix * matrix(identity)

    def RotationX(self, r):
        array = [
            [1, 0, 0, 0],
            [0, round(math.cos(r), 7), round(-math.sin(r), 7), 0],
            [0, round(math.sin(r), 7), round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        self.matrix = self.matrix * matrix(array)

    def RotationY(self, r):
        array = [
            [round(math.cos(r), 7), 0, round(math.sin(r), 7), 0],
            [0, 1, 0, 0],
            [round(-math.sin(r), 7), 0, round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        self.matrix = self.matrix * matrix(array)

    def RotationZ(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        self.matrix = self.matrix * matrix(array)

    def RotationZ(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        self.matrix = self.matrix * matrix(array)

    def Shearing(self, xy, xz, yx, yz, zx, zy):
        array = [[1, xy, xz, 0], [yx, 1, yz, 0], [zx, zy, 1, 0], [0, 0, 0, 1]]
        self.matrix = self.matrix * matrix(array)

    def reflect(self, other):
        return self - other * 2 * self.dot(other)


class Point(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)


class Vector(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0)

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

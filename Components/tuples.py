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


class Color():
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        red = self.red + other.red
        green = self.green + other.green
        blue = self.blue + other.blue

        return Color(red, green, blue)

    def __sub__(self, other):
        red = self.red - other.red
        green = self.green - other.green
        blue = self.blue - other.blue

        return Color(red, green, blue)

    def __eq__(self, other):
        if (self.red == other.red and
            self.green == other.green and
                self.blue == other.blue):
            return True
        return False

    def __mul__(self, scalar):
        red = self.red * scalar
        green = self.green * scalar
        blue = self.blue * scalar
        return Color(red, green, blue)

    def show(self):
        return (self.red, self.green, self.blue)

    def hadamard(self, other):
        red = self.red * other.red
        green = self.green * other.green
        blue = self.blue * other.blue

        return Color(red, green, blue)

    def to_rgb(self):
        r = str(clamp(math.ceil(self.red * 255), 0, 255))
        g = str(clamp(math.ceil(self.green * 255), 0, 255))
        b = str(clamp(math.ceil(self.blue * 255), 0, 255))

        return ' '.join([r, g, b])

    def __round__(self, idx=4):
        return Color(round(self.red, idx), round(self.green, idx), round(self.blue, idx))

    def __str__(self):
        return str((self.red, self.green, self.blue))


def clamp(n: float, minn: int, maxn: int) -> int:
    return int(max(min(maxn, n), minn))

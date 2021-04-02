from chapter1 import *
from Matrice import *
from math import pi, sin, cos

# i want to refacot these to be functions in the matrix class


class translation(matrix):  # switch to stranslation at some point
    def __init__(self, x, y, z):
        identity = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        super().__init__(identity)


class scaling(matrix):
    def __init__(self, x, y, z):
        identity = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
        super().__init__(identity)


class RotationX(matrix):
    def __init__(self, r):
        array = [
            [1, 0, 0, 0],
            [0, round(math.cos(r), 7), round(-math.sin(r), 7), 0],
            [0, round(math.sin(r), 7), round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationY(matrix):
    def __init__(self, r):
        array = [
            [round(math.cos(r), 7), 0, round(math.sin(r), 7), 0],
            [0, 1, 0, 0],
            [round(-math.sin(r), 7), 0, round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationZ(matrix):
    def __init__(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationZ(matrix):
    def __init__(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class Shearing(matrix):
    def __init__(self, xy, xz, yx, yz, zx, zy):
        super().__init__(
            [[1, xy, xz, 0], [yx, 1, yz, 0], [zx, zy, 1, 0], [0, 0, 0, 1]])

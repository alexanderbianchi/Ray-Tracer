import math
from math import pi
from raytracer.components.tuples import *
import copy


EPSILON = 0.00001

#Matrix and Transformations


class Matrix():
    def __init__(self, array):
        self.matrix = list(list(x) for x in array)
        self.width = len(array[0])
        self.height = len(array)

    def isTuple(self):
        return False

    def __getitem__(self, y):
        return self.matrix[y]

    def __str__(self):
        return str(self.matrix)

    def __eq__(self, other):
        if self.width != other.width or self.height != other.height:
            return False
        for i in range(self.height):
            for j in range(self.width):
                if abs(self[i][j] - other[i][j]) > EPSILON:
                    return False
        return True

    def __mul__(self, other):

        if other.isTuple():
            arr = []
            for i in range(self.height):
                temp = 0
                for j in range(self.width):
                    temp += self[i][j] * other[j]
                arr.append(temp)
            return Tuple(*arr)

        else:
            c = [[0 for i in range(other.width)] for j in range(self.height)]
            for i in range(self.height):

                for j in range(other.width): 

                    point = (self[i][0] * other[0][j] +
                             self[i][1] * other[1][j] +
                             self[i][2] * other[2][j] +
                             self[i][3] * other[3][j])
                    c[i][j] = point

            return Matrix(c)

    def transpose(self):
        temp = [[0 for i in range(self.width)]
                for j in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                temp[j][i] = self[i][j]

        return Matrix(temp)

    def determinant(self):
        if self.width == 2 and self.height == 2:
            return self.matrix[0][0] * self.matrix[1][1] \
                - self.matrix[1][0] * self.matrix[0][1]
        else:
            det = 0
            for i in range(len(self.matrix[0])):
                det += self.cofactor(0, i) * self.matrix[0][i]
            return det

    def submatrix(self, row, col):
        array = copy.deepcopy(self.matrix)
        array.pop(row)
        for i in array:
            i.pop(col)
        return Matrix(array)

    def minor(self, row, col):
        return self.submatrix(row, col).determinant()

    def cofactor(self, row, col):
        x = self.minor(row, col)
        if (row+col) % 2 == 1:
            x = -x
        return x

    def isInvertable(self):
        return self.determinant() != 0

    def inverse(self):
        det = self.determinant()

        if not self.isInvertable():
            return False

        array = [([0] * self.height) for _ in range(self.height)]

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                c = self.cofactor(i, j)
                array[j][i] = c/det

        return Matrix(array)


class Translation(Matrix):  
    def __init__(self, x, y, z):
        identity = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        super().__init__(identity)


class Scaling(Matrix):
    def __init__(self, x, y, z):
        identity = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
        super().__init__(identity)


class RotationX(Matrix):
    def __init__(self, r):
        array = [
            [1, 0, 0, 0],
            [0, round(math.cos(r), 7), round(-math.sin(r), 7), 0],
            [0, round(math.sin(r), 7), round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationY(Matrix):
    def __init__(self, r):
        array = [
            [round(math.cos(r), 7), 0, round(math.sin(r), 7), 0],
            [0, 1, 0, 0],
            [round(-math.sin(r), 7), 0, round(math.cos(r), 7), 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationZ(Matrix):
    def __init__(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class RotationZ(Matrix):
    def __init__(self, r):
        array = [
            [math.cos(r), -math.sin(r), 0, 0],
            [math.sin(r), math.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        super().__init__(array)


class Shearing(Matrix):
    def __init__(self, xy, xz, yx, yz, zx, zy):
        super().__init__(
            [[1, xy, xz, 0], [yx, 1, yz, 0], [zx, zy, 1, 0], [0, 0, 0, 1]])

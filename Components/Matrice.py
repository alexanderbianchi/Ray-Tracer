import math
from math import pi
from chapter1 import *
import copy

EPSILON = 0.001


class matrix():
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
                    print(self[i][j] - other[i][j])
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

                for j in range(other.width):  # invert it then use the rows?

                    point = (self[i][0] * other[0][j] +
                             self[i][1] * other[1][j] +
                             self[i][2] * other[2][j] +
                             self[i][3] * other[3][j])
                    c[i][j] = point

            return matrix(c)

    def transpose(self):
        temp = [[0 for i in range(self.width)]
                for j in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                temp[j][i] = self[i][j]

        return matrix(temp)

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
        return matrix(array)

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
                array[j][i] = round(c/det, 5)

        return matrix(array)

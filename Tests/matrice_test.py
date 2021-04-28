from imports import *

def test_matrix():
    array = [[1, 2, 3, 4, 5],
             [6, 7, 8, 9, 10],
             [1, 2, 3, 4, 5]]
    marix = Matrix(array)

    assert marix[2][4] == 5


def test_equal_test():
    array = [[1, 2, 3, 4, 5],
             [6, 7, 8, 9, 10],
             [1, 2, 3, 4, 5]]
    one = Matrix(array)
    two = Matrix(array)
    array2 = [[1, 2, 3, 4, 5],
              [6, 7, 8, 9, 10],
              [1, 2, 3, 4, 6]]
    three = Matrix(array2)
    assert one == two
    assert two != three


def test_multiply():
    array = [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 8, 7, 6],
             [5, 4, 3, 2]]

    array1 = [[-2, 1, 2, 3],
              [3, 2, 1, -1],
              [4, 3, 6, 5],
              [1, 2, 7, 8]]

    answer = [[20, 22, 50, 48],
              [44, 54, 114, 108],
              [40, 58, 110, 102],
              [16, 26, 46, 42]]

    test = Matrix(array) * Matrix(array1)
    assert Matrix(answer) == test


def test_identity_mul():
    identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    array = [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 8, 7, 6],
             [5, 4, 3, 2]]
    test = Matrix(array) * Matrix(identity)
    assert test == Matrix(array)


def test_transpose():
    array = [[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]]
    answer = [[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]]
    assert Matrix(array).transpose() == Matrix(answer)


def test_2by2_determinant():
    array = [[1, 5], [-3, 2]]
    mat = Matrix(array)
    assert mat.determinant() == 17


def test_submatrix_3x3():
    array = [[1, 5, 0], [-3, 2, 7], [0, 6, 3]]
    answer = [[-3, 2], [0, 6]]
    assert Matrix(array).submatrix(0, 2) == Matrix(answer)


def test_submatrix_4x4():
    array = [[6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]]
    answer = [[6, 1, 6], [-8, 8, 6], [-7, -1, 1]]
    assert Matrix(array).submatrix(2, 1) == Matrix(answer)


def test_tuple_multiply():
    array = [[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]]
    tup = Tuple(1, 2, 3, 1)
    assert Matrix(array) * tup == Tuple(18, 24, 33, 1)


def test_minor():
    array = [[3, 5, 0], [2, -1, -7], [6, -1, 5]]
    assert Matrix(array).minor(1, 0) == 25


def test_cofactor():
    array = [[3, 5, 0], [2, -1, -7], [6, -1, 5]]
    assert Matrix(array).cofactor(1, 0) == -25
    assert Matrix(array).minor(1, 0) == 25
    assert Matrix(array).cofactor(0, 0) == -12
    assert Matrix(array).minor(0, 0) == -12


def test_determinant():
    array = [[1, 2, 6], [-5, 8, -4], [2, 6, 4]]
    assert Matrix(array).determinant() == -196


def test_determinant_4x4():
    array = [[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]]
    assert Matrix(array).determinant() == -4071


def test_inverse():
    array = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8],
                    [7, 7, -6, -7], [1, -3, 7, 4]])
    answer = Matrix([
        [0.21805, 0.45113, 0.24060, -0.04511],
        [-0.80827, -1.45677, -0.44361, 0.52068],
        [-0.07895, -0.22368, -0.05263, 0.19737],
        [-0.52256, -0.81391, -0.30075, 0.30639],
    ])
    test = array.inverse()

    assert test == answer

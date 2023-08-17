# see http://jsfiddle.net/dFrHS/1/
# http://math.stackexchange.com/questions/296794/finding-the-transform-matrix-from-4-projected-points-with-javascript


# create a 4x4 transformation matrix based on the movement of 4 points (corner pin)
# s-variables are the 4 points before the transform and d variables after
def computeProjectionMatrix4FromCornerPin(x1s, y1s, x1d, y1d,
                                          x2s, y2s, x2d, y2d,
                                          x3s, y3s, x3d, y3d,
                                          x4s, y4s, x4d, y4d):
    x1s = float(x1s)
    x2s = float(x2s)
    x3s = float(x3s)
    x4s = float(x4s)
    x1d = float(x1d)
    x2d = float(x2d)
    x3d = float(x3d)
    x4d = float(x4d)
    y1s = float(y1s)
    y2s = float(y2s)
    y3s = float(y3s)
    y4s = float(y4s)
    y1d = float(y1d)
    y2d = float(y2d)
    y3d = float(y3d)
    y4d = float(y4d)

    t3 = computeProjectionMatrix3FromCornerPin(x1s, y1s, x1d, y1d,
                                               x2s, y2s, x2d, y2d,
                                               x3s, y3s, x3d, y3d,
                                               x4s, y4s, x4d, y4d)
    for i in range(0, 9):
        t3[i] = t3[i] / t3[8]

    t4 = [t3[0], t3[1], 0, t3[2],
          t3[3], t3[4], 0, t3[5],
          0, 0, 1, 0,
          t3[6], t3[7], 0, t3[8]]
    return t4


def matrix4ToString(tm):
    result = str(tm[0]) + " " + str(tm[1]) + " " + str(tm[2]) + " " + str(tm[3]) + "\n" + str(tm[4]) + " " + str(
        tm[5]) + " " + str(tm[6]) + " " + str(tm[7]) + "\n" + str(tm[8]) + " " + str(tm[9]) + " " + str(
        tm[10]) + " " + str(tm[11]) + "\n" + str(tm[12]) + " " + str(tm[13]) + " " + str(tm[14]) + " " + str(tm[15])
    return result


def multiply3MatrixAnd3Matrix(a, b):  # multiply two matrices
    c = [0] * 9  # list of length 9
    for i in range(0, 3):
        for j in range(0, 3):
            cij = 0
            for k in range(0, 3):
                cij += a[3 * i + k] * b[3 * k + j]
            c[3 * i + j] = cij
    return c


def multiply3MatrixAnd3Vector(m, v):  # multiply matrix and vector
    result = [
        m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
        m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
        m[6] * v[0] + m[7] * v[1] + m[8] * v[2]
    ]
    return result


def computeAdjugateMatrix(m):  # Compute the adjugate of m
    result = [m[4] * m[8] - m[5] * m[7], m[2] * m[7] - m[1] * m[8], m[1] * m[5] - m[2] * m[4],
              m[5] * m[6] - m[3] * m[8], m[0] * m[8] - m[2] * m[6], m[2] * m[3] - m[0] * m[5],
              m[3] * m[7] - m[4] * m[6], m[1] * m[6] - m[0] * m[7], m[0] * m[4] - m[1] * m[3]
              ]
    return result


def basisToMatrix3(x1, y1, x2, y2, x3, y3, x4, y4):
    m = [
        x1, x2, x3,
        y1, y2, y3,
        1, 1, 1
    ]
    v = multiply3MatrixAnd3Vector(computeAdjugateMatrix(m), [x4, y4, 1])
    result = multiply3MatrixAnd3Matrix(m, [
        v[0], 0, 0,
        0, v[1], 0,
        0, 0, v[2]
    ])
    return result


def computeProjectionMatrix3FromCornerPin(
        x1s, y1s, x1d, y1d,
        x2s, y2s, x2d, y2d,
        x3s, y3s, x3d, y3d,
        x4s, y4s, x4d, y4d
):
    s = basisToMatrix3(x1s, y1s, x2s, y2s, x3s, y3s, x4s, y4s)
    d = basisToMatrix3(x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
    return multiply3MatrixAnd3Matrix(d, computeAdjugateMatrix(s))

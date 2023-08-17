import math


# 2D transformation matrices are represented as tuple (a1,a2,a3,a4,a5,a6)
# which correspond to this transformation matrix:
# a1 a2 a3
# a4 a5 a6 
#  0  0  1
# see http://stackoverflow.com/questions/1114257/transform-a-triangle-to-another-triangle

def affineTransformFromMovementOfThreePoints(p1Before, p2Before, p3Before, p1After, p2After, p3After):
    x11 = p1Before[0]
    x12 = p1Before[1]
    x21 = p2Before[0]
    x22 = p2Before[1]
    x31 = p3Before[0]
    x32 = p3Before[1]
    y11 = p1After[0]
    y12 = p1After[1]
    y21 = p2After[0]
    y22 = p2After[1]
    y31 = p3After[0]
    y32 = p3After[1]

    a1 = ((y11 - y21) * (x12 - x32) - (y11 - y31) * (x12 - x22)) / (
            (x11 - x21) * (x12 - x32) - (x11 - x31) * (x12 - x22))
    a2 = ((y11 - y21) * (x11 - x31) - (y11 - y31) * (x11 - x21)) / (
            (x12 - x22) * (x11 - x31) - (x12 - x32) * (x11 - x21))
    a3 = y11 - a1 * x11 - a2 * x12
    a4 = ((y12 - y22) * (x12 - x32) - (y12 - y32) * (x12 - x22)) / (
            (x11 - x21) * (x12 - x32) - (x11 - x31) * (x12 - x22))
    a5 = ((y12 - y22) * (x11 - x31) - (y12 - y32) * (x11 - x21)) / (
            (x12 - x22) * (x11 - x31) - (x12 - x32) * (x11 - x21))
    a6 = y12 - a4 * x11 - a5 * x12

    matrix = (a1, a2, a3,
              a4, a5, a6)
    # third row 0, 0, 1 is skipped

    return matrix


# see best http://stackoverflow.com/tags/affinetransform/info
def getTransformComponents(matrix):
    # Matrix:
    # a b x
    # c d y

    a = matrix[0]
    b = matrix[1]
    x = matrix[2]
    c = matrix[3]
    d = matrix[4]
    y = matrix[5]

    if a * d < 0:
        if a < 0:
            flip = 1
            a = -a
            b = -b
        else:
            flip = 2
            d = -d
            c = -c
    else:
        flip = 0

    rx = math.atan2(-b, a)
    ry = math.atan2(c, d)

    if abs(rx) < abs(ry):
        r = rx
        skew_rx = 0
        skew_ry = ry - rx
        scale_x = math.sqrt(a * a + b * b)
        scale_y = d / (math.cos(r) - math.sin(r) * math.tan(skew_ry))
    else:
        r = ry
        skew_ry = 0
        skew_rx = ry - rx
        scale_y = math.sqrt(d * d + c * c)
        scale_x = a / (math.cos(r) + math.sin(r) * math.tan(skew_rx))

    if 1 == flip:
        scale_x = -scale_x
    if 2 == flip:
        scale_y = -scale_y

    result = {
        'translation': (x, y),
        'rotation': r,
        'shear': (skew_rx, skew_ry),
        'scale': (scale_x, scale_y)
    }

    return result


# ALTERNATIVE
# see also http://stackoverflow.com/questions/4361242/extract-rotation-scale-values-from-2d-transformation-matrix
def getTranslationFromAffineTransformation(matrix):
    return matrix[2], matrix[5]


def getRotationFromAffineTransformation(matrix):
    c = matrix[3]
    d = matrix[4]
    rotation = math.atan(c / d)
    return rotation


def getScaleFromAffineTransformation(matrix):
    a = matrix[0]
    b = matrix[1]
    c = matrix[3]
    d = matrix[4]
    scaleX = math.sqrt(a * a + b * b)
    scaleY = math.sqrt(c * c + d * d)
    if a < 0:
        scaleX = scaleX * -1
    if b < 0:
        scaleY = scaleY * -1

    return scaleX, scaleY

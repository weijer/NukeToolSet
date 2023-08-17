import projectiveTransformation
import transformMatrix4Data


def cp2TransformMatrix(cpData, referenceFrame):
    x1 = cpData.getPointValues(0, 'x')
    y1 = cpData.getPointValues(0, 'y')
    x2 = cpData.getPointValues(1, 'x')
    y2 = cpData.getPointValues(1, 'y')
    x3 = cpData.getPointValues(2, 'x')
    y3 = cpData.getPointValues(2, 'y')
    x4 = cpData.getPointValues(3, 'x')
    y4 = cpData.getPointValues(3, 'y')

    referenceIndex = getFrameIndex(x1, referenceFrame)

    transformMatrix = transformMatrix4Data.TransformMatrix4()
    if len({len(x1), len(x2), len(x3), len(x4), len(y1), len(y2), len(y3), len(y4)}) > 1:
        raise Exception('all corners must have the same amount of keyframes')

    for i in range(0, len(x1)):
        frameNumber = x1[i][0]
        # check times of all 4 entries are equal
        if len({x1[i][0], x2[i][0], x3[i][0], x4[i][0], y1[i][0], y2[i][0], y3[i][0], y4[i][0]}) > 1:
            raise Exception('times for keyframes of all four corners must be identical')

        matrix = projectiveTransformation.computeProjectionMatrix4FromCornerPin(
            x1[referenceIndex][1], y1[referenceIndex][1], x1[i][1], y1[i][1],
            x2[referenceIndex][1], y2[referenceIndex][1], x2[i][1], y2[i][1],
            x3[referenceIndex][1], y3[referenceIndex][1], x3[i][1], y3[i][1],
            x4[referenceIndex][1], y4[referenceIndex][1], x4[i][1], y4[i][1])

        transformMatrix.setKey((frameNumber, matrix))

    return transformMatrix


def getFrameIndex(pointValues, frameIndex):
    for i in range(0, len(pointValues)):
        if pointValues[i][0] == frameIndex:
            return i
    raise Exception("tracking data doesn't contain tracking data for frame " + str(
        frameIndex) + ".\nPlease choose another reference frame.")

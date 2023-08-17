import math
import affineTransformation


class TransformData(object):
    """abstract base class for transform data"""

    def hasPositionData(self):
        raise NotImplementedError('hasPositionData not implemented')

    def hasScaleData(self):
        raise NotImplementedError('hasScaleData not implemented')

    def hasRotationData(self):
        raise NotImplementedError('hasRotationData not implemented')

    def hasShearData(self):
        raise NotImplementedError('hasShearData not implemented')

    def getPositionValues(self, coordinate):
        """for coordinate in 'x', 'y' returns a list of (frame,value) tuples"""
        raise NotImplementedError('getPositionValues not implemented')

    def getScaleValues(self, coordinate):
        """for coordinate in 'x', 'y' returns a list of (frame,value) tuples"""
        raise NotImplementedError('getScaleValues not implemented')

    def getRotationValues(self):
        """returns a list of (frame,value) tuples"""
        raise NotImplementedError('getRotationValues not implemented')

    def getShearValues(self, coordinate):
        """for coordinate in 'x', 'y' returns a list of (frame,value) tuples"""
        raise NotImplementedError('getShearValues not implemented')


class TransformDataAsLists(TransformData):
    """transform data that represents position, scale rotation and shear as a dictionary of lists"""

    def __init__(self):
        self.data = {"position": {'x': [], 'y': []},
                     "rotation": [],
                     "scale": {'x': [], 'y': []},
                     "shear": {'x': [], 'y': []}
                     }

    def hasPositionData(self):
        hasXValues = len(self.data["position"]['x']) > 0
        hasYValues = len(self.data["position"]['y']) > 0
        return hasXValues or hasYValues

    def hasScaleData(self):
        hasXValues = len(self.data["scale"]['x']) > 0
        hasYValues = len(self.data["scale"]['y']) > 0
        return hasXValues or hasYValues

    def hasRotationData(self):
        hasValues = len(self.data["rotation"]) > 0
        return hasValues

    def hasShearData(self):
        hasXValues = len(self.data["shear"]['x']) > 0
        hasYValues = len(self.data["shear"]['y']) > 0
        return hasXValues or hasYValues

    def getPositionValues(self, coordinate):
        assert (coordinate in ['x', 'y'])
        return self.data["position"][coordinate]

    def getScaleValues(self, coordinate):
        assert (coordinate in ['x', 'y'])
        return self.data["scale"][coordinate]

    def getRotationValues(self):
        return self.data["rotation"]

    def getShearValues(self, coordinate):
        assert (coordinate in ['x', 'y'])
        return self.data["shear"][coordinate]


class TransformDataFromCornerPinData(TransformDataAsLists):
    """transform data that is obtained by converting corner pin data"""

    def __init__(self, cpData):
        super(TransformDataFromCornerPinData, self).__init__()

        self.__importCpData(cpData)

    def __importCpData(self, cpData):
        x1 = cpData.getPointValues(0, 'x')
        y1 = cpData.getPointValues(0, 'y')
        x2 = cpData.getPointValues(1, 'x')
        y2 = cpData.getPointValues(1, 'y')
        x3 = cpData.getPointValues(2, 'x')
        y3 = cpData.getPointValues(2, 'y')
        x4 = cpData.getPointValues(3, 'x')
        y4 = cpData.getPointValues(3, 'y')

        if len({len(x1), len(x2), len(x3), len(x4), len(y1), len(y2), len(y3), len(y4)}) > 1:
            raise Exception('all corners must have the same amount of keyframes')

        xPosition = []
        yPosition = []
        rotation = []
        xScale = []
        yScale = []
        xShear = []
        yShear = []
        for i in range(0, len(x1)):
            frameNumber = x1[i][0]
            # check times of all 4 entries are equal
            if len({x1[i][0], x2[i][0], x3[i][0], x4[i][0], y1[i][0], y2[i][0], y3[i][0], y4[i][0]}) > 1:
                raise Exception('times for keyframes of all four corners must be identical')

            # compute position
            xVal = (x1[i][1] + x2[i][1] + x3[i][1] + x4[i][1]) / 4
            yVal = (y1[i][1] + y2[i][1] + y3[i][1] + y4[i][1]) / 4

            xPosition.append((frameNumber, xVal))
            yPosition.append((frameNumber, yVal))

            # compute tranformation matrix
            refI = 0
            prevX = xPosition[refI][1]
            prevY = xPosition[refI][1]

            p1Before = [x1[refI][1] - prevX, y1[refI][1] - prevY]
            p2Before = [x2[refI][1] - prevX, y2[refI][1] - prevY]
            p3Before = [x3[refI][1] - prevX, y3[refI][1] - prevY]
            p1After = [x1[i][1] - prevX, y1[i][1] - prevY]
            p2After = [x2[i][1] - prevX, y2[i][1] - prevY]
            p3After = [x3[i][1] - prevX, y3[i][1] - prevY]

            affineTrans = affineTransformation.affineTransformFromMovementOfThreePoints(
                p1Before, p2Before, p3Before, p1After, p2After, p3After)
            transforms = affineTransformation.getTransformComponents(affineTrans)

            xScale.append((frameNumber, transforms['scale'][0]))
            yScale.append((frameNumber, transforms['scale'][1]))
            rotation.append((frameNumber, math.degrees(transforms['rotation'])))
            xShear.append((frameNumber, transforms['shear'][0]))
            yShear.append((frameNumber, transforms['shear'][1]))

        self.data['position']['x'] = xPosition
        self.data['position']['y'] = yPosition
        self.data['scale']['x'] = xScale
        self.data['scale']['y'] = yScale
        self.data['rotation'] = rotation
        self.data['shear']['x'] = xShear
        self.data['shear']['y'] = yShear
        # print(pprint.pformat(self.data))

import re
import pprint

try:
    from PySide import QtGui

    clipboardModule = QtGui
except:
    from PySide2 import QtWidgets

    clipboardModule = QtWidgets


class CornerPinData(object):
    """abstract base class for corner pin data"""

    def getPointValues(self, pointIndex, coordinate):
        """for pointIndex in 0,1,2,3 and coordinate in 'x', 'y' returns a list of (frame,value) tuples"""
        raise NotImplementedError('getPoint not implemented')


class FileFormatError(Exception):
    """Invalid File Format Error"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class CornerPinDataAsList(CornerPinData):
    def __init__(self):
        self.points = [{'x': [], 'y': []},
                       {'x': [], 'y': []},
                       {'x': [], 'y': []},
                       {'x': [], 'y': []}]

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(self.points)

    def getPointValues(self, pointIndex, coordinate):
        assert (coordinate in ['x', 'y'])
        assert (pointIndex in [0, 1, 2, 3])

        return self.points[pointIndex][coordinate]


# Corner pin data parsed from a text as it is stored in a mocha corner pin file for nuke file
class CornerPinDataFromNukeCornerPinText(CornerPinDataAsList):

    def __init__(self, cornerPinText):
        super(CornerPinDataFromNukeCornerPinText, self).__init__()
        self.demoLimitationInfo = "In trial mode only the first 20 frames of tracking data are imported."
        self.__parseMochaNukeData(cornerPinText)

    def __parseMochaNukeData(self, trackingData):
        # input curveData has the form "xFrame Value" like this "x0 472.276 x1 472.276 x2 472.276..."
        # but can also be more complex, see: https://github.com/julik/tickly/blob/master/lib/tickly/curve.rb#L51
        # Nuke saves curves very efficiently. x(keyframe_number) means that an
        # uninterrupted sequence of values will start, after which values follow.
        # When the curve is interrupted in some way a new x(keyframe_number) will
        # signify that we skip to that specified keyframe and the curve continues
        # from there, in gap size defined by the last fragment. That is,
        # x1 1 x3 2 3 4 will place 2, 3 and 4 at 2-frame increments.
        # Thanks to Michael Lester for explaining this.
        def curveDataToAnimationKeys(curveData):
            keyValueList = []
            simpleList = curveData.split()

            timeIncrement = 1
            nextKeyframeTime = 1

            for val in simpleList:

                if val[0] == "x":
                    # we have a keyframe time
                    nextKeyframeTime = float(val[1:])
                    if len(keyValueList) > 0:
                        previousKeyframeTime = keyValueList[-1][0]
                        timeIncrement = nextKeyframeTime - previousKeyframeTime

                else:
                    # we have a keyframe value
                    value = float(val)
                    frameNumber = nextKeyframeTime
                    keyValueList.append((frameNumber, value))

                    nextKeyframeTime += timeIncrement

            return keyValueList

        def parseCornerPoint(pointName, _trackingData):
            parseDataRegExp = re.compile(pointName + r"\s*{\s*{\s*curve\s*([^}]*)}\s*{\s*curve\s*([^}]*)}\s*}")
            trackingDataParse = parseDataRegExp.search(_trackingData)
            if trackingDataParse is None:
                raise FileFormatError(
                    "invalid tracking data - please use corner pin data exported from mocha Pro with the "
                    "format set to 'Nuke Corner Pin (*.nk)'")

            pointDataX = trackingDataParse.group(1)
            pointDataY = trackingDataParse.group(2)

            pointData = {'x': curveDataToAnimationKeys(pointDataX), 'y': curveDataToAnimationKeys(pointDataY)}
            return pointData

        self.points[0] = parseCornerPoint("to1", trackingData)
        self.points[1] = parseCornerPoint("to2", trackingData)
        self.points[2] = parseCornerPoint("to3", trackingData)
        self.points[3] = parseCornerPoint("to4", trackingData)


# Corner pin data parsed from a mocha corner pin file for nuke
class CornerPinDataFromNukeCornerPinFile(CornerPinDataFromNukeCornerPinText):
    def __init__(self, filename):
        trackingDataFile = open(filename, mode='r')
        trackingData = trackingDataFile.read()
        trackingDataFile.close()
        super(CornerPinDataFromNukeCornerPinFile, self).__init__(trackingData)


# Corner pin data parsed from the clipboard (must be in *.nk format)
class CornerPinDataFromClipboard(CornerPinDataFromNukeCornerPinText):
    def __init__(self):
        trackingData = clipboardModule.QApplication.clipboard().text()
        super(CornerPinDataFromClipboard, self).__init__(trackingData)

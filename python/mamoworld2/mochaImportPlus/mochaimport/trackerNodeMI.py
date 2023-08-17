import nuke
import cornerPinData
import loadTrackingDataTab
import trackingDataConversion


# Tracker 3 --> old node type

def createTracker3NodeMI():
    tracker3Node = nuke.createNode('Tracker3')

    loadTrackingDataTab.addLoadTrackingDataUI(
        tracker3Node,
        "mochaimport.trackerNodeMI.loadTracker3TrackingDataFromFilePopup(nuke.thisNode())",
        "mochaimport.trackerNodeMI.loadTracker3TrackingDataFromClipboard(nuke.thisNode())")

    tracker3Node['enable1'].setValue('true')
    tracker3Node['enable2'].setValue('true')
    tracker3Node['enable3'].setValue('true')
    tracker3Node['enable4'].setValue('true')

    tracker3Node['label'].setValue('MochaImportPlus')
    return tracker3Node


def loadTracker3TrackingDataFromFilePopup(tracker3Node):
    try:
        trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')
        if trackingDataFilePath is None:
            return
        trackingData = cornerPinData.CornerPinDataFromNukeCornerPinFile(trackingDataFilePath)
        setCornerPinDataForTracker3Node(tracker3Node, trackingData)

    except IOError as e:
        nuke.message(
            "Could not read file {0}:\n\nI/O error({1}): {2}".format(trackingDataFilePath, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message("Could not read file {0}:\n\nInvalid File Format: {1}".format(trackingDataFilePath, e.message))


def loadTracker3TrackingDataFromClipboard(tracker3Node):
    try:
        trackingData = cornerPinData.CornerPinDataFromClipboard()
        setCornerPinDataForTracker3Node(tracker3Node, trackingData)
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))


def setCornerPinDataForTracker3Node(trackerNode, cpData):
    setCornerPinPointDataForTracker3TrackPoint(trackerNode['track1'], cpData, 0)
    setCornerPinPointDataForTracker3TrackPoint(trackerNode['track2'], cpData, 1)
    setCornerPinPointDataForTracker3TrackPoint(trackerNode['track3'], cpData, 2)
    setCornerPinPointDataForTracker3TrackPoint(trackerNode['track4'], cpData, 3)


def setCornerPinPointDataForTracker3TrackPoint(trackpoint, cpData, pointIndex):
    xData = trackingDataConversion.tuplesToAnimationKeys(cpData.getPointValues(pointIndex, 'x'))
    yData = trackingDataConversion.tuplesToAnimationKeys(cpData.getPointValues(pointIndex, 'y'))

    trackpoint.setAnimated()

    trackpoint.animation(0).clear()
    trackpoint.animation(1).clear()

    trackpoint.animation(0).addKey(xData)
    trackpoint.animation(1).addKey(yData)


# Tracker 4 --> new node type

def createTracker4NodeMI():
    tracker4Node = nuke.createNode('Tracker4')

    loadTrackingDataTab.addLoadTrackingDataUI(
        tracker4Node,
        "mochaimport.trackerNodeMI.loadTracker4TrackingDataFromFilePopup(nuke.thisNode())",
        "mochaimport.trackerNodeMI.loadTracker4TrackingDataFromClipboard(nuke.thisNode())")

    for _ in range(0, 4):
        tracker4Node['add_track'].execute()

    tracker4Node['label'].setValue('MochaImportPlus')

    return tracker4Node


def ensureTracker4NodeHasAtLeastFourTracks(trackerNode):
    numTracks = getNumberOfTracks(trackerNode)
    tracksToCreate = 4 - numTracks
    if tracksToCreate > 0:
        for _ in range(tracksToCreate):
            trackerNode['add_track'].execute()


def loadTracker4TrackingDataFromFilePopup(tracker4Node):
    try:
        trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')
        if trackingDataFilePath is None:
            return
        trackingData = cornerPinData.CornerPinDataFromNukeCornerPinFile(trackingDataFilePath)
        setCornerPinDataForTracker4Node(tracker4Node, trackingData)
    except IOError as e:
        nuke.message(
            "Could not read file {0}:\n\nI/O error({1}): {2}"
            .format(trackingDataFilePath, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message("Could not read file {0}:\n\nInvalid File Format: {1}"
                     .format(trackingDataFilePath, e.message))


def loadTracker4TrackingDataFromClipboard(tracker4Node):
    try:
        trackingData = cornerPinData.CornerPinDataFromClipboard()
        setCornerPinDataForTracker4Node(tracker4Node, trackingData)
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))


def setCornerPinDataForTracker4Node(tracker4Node, cpData):
    ensureTracker4NodeHasAtLeastFourTracks(tracker4Node)

    xColumnIndex = 2
    yColumnIndex = 3
    translationColumnIndex = 6
    rotationColumnIndex = 7
    scaleColumnIndex = 8

    numColumns = 31

    clearAnimationOfFirstFourTracks(tracker4Node)

    track = tracker4Node['tracks']

    progress = nuke.ProgressTask('write tracking data')
    for i in [0, 1, 2, 3]:

        progress.setMessage('data for corner ' + str(i + 1))

        track.setAnimated(numColumns * i + xColumnIndex)
        track.setAnimated(numColumns * i + yColumnIndex)

        xData = cpData.getPointValues(i, 'x')
        yData = cpData.getPointValues(i, 'y')
        for (time, xVal) in xData:
            track.setValueAt(xVal, time, numColumns * i + xColumnIndex)
        for (time, yVal) in yData:
            track.setValueAt(yVal, time, numColumns * i + yColumnIndex)

        track.setValue(1, numColumns * i + translationColumnIndex)
        track.setValue(1, numColumns * i + rotationColumnIndex)
        track.setValue(1, numColumns * i + scaleColumnIndex)

        progress.setProgress(i * 25)


def clearAnimationOfFirstFourTracks(tracker4Node):
    xColumnIndex = 2
    yColumnIndex = 3
    numColumns = 31

    for i in [0, 1, 2, 3]:
        tracker4Node['tracks'].clearAnimated(numColumns * i + xColumnIndex)
        tracker4Node['tracks'].clearAnimated(numColumns * i + yColumnIndex)


# see http://forums.thefoundry.co.uk/phpBB2/viewtopic.php?p=42795
def getTrackNames(tracker4Node):
    k = tracker4Node['tracks']
    s = tracker4Node['tracks'].toScript().split(' \n} \n{ \n ')
    s.pop(0)
    ss = str(s)[2:].split('\\n')
    if ss:
        ss.pop(-1)
    if ss:
        ss.pop(-1)
    outList = []
    for i in ss:
        outList.append(i.split('"')[1])
    return outList


def getNumberOfTracks(tracker4Node):
    result = len(getTrackNames(tracker4Node))

    return result

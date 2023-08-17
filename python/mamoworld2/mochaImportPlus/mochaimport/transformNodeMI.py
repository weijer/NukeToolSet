import nuke
import transformData
import trackingDataConversion
import cornerPinData
import loadTrackingDataTab


class NoImportOptionChosen(Exception):
    def __init__(self):
        self.message = "Please choose at least one type of data that you want to import."


def createTransformNodeMI():
    transformNode = nuke.createNode('Transform')
    loadTrackingDataTab.addLoadTrackingDataUI(
        transformNode,
        "mochaimport.transformNodeMI.loadTransformTrackingDataFromFilePopup(nuke.thisNode())",
        "mochaimport.transformNodeMI.loadTransformTrackingDataFromClipboard(nuke.thisNode())",
    )

    for dataName in ["translate", "rotate", "scale", "skew"]:
        createTrackingDataOptionKnob(dataName, transformNode)

    transformNode['label'].setValue('MochaImportPlus')


def createTrackingDataOptionKnob(name, node):
    knob = nuke.Boolean_Knob("import" + name + "data", "import " + name + " data")
    knob.setTooltip("whether loading the mocha data generates keyframes for " + name)
    knob.setValue(True)
    knob.setFlag(nuke.STARTLINE)
    node.addKnob(knob)


def loadTransformTrackingDataFromFilePopup(transformNode):
    try:
        checkIfAnyImportOptionChosen(transformNode)
        trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')
        if trackingDataFilePath is None:
            return
        cpData = cornerPinData.CornerPinDataFromNukeCornerPinFile(trackingDataFilePath)
        tfData = transformData.TransformDataFromCornerPinData(cpData)
        setTransformDataForTransformNode(transformNode, tfData)
    except IOError as e:
        nuke.message(
            "Could not read file {0}:\n\nI/O error({1}): {2}".format(trackingDataFilePath, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message("Could not read file {0}:\n\nInvalid File Format: {1}".format(trackingDataFilePath, e.message))
    except NoImportOptionChosen as e:
        nuke.message(e.message)


def loadTransformTrackingDataFromClipboard(transformNode):
    try:
        checkIfAnyImportOptionChosen(transformNode)

        cpData = cornerPinData.CornerPinDataFromClipboard()
        tfData = transformData.TransformDataFromCornerPinData(cpData)
        setTransformDataForTransformNode(transformNode, tfData)
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))
    except NoImportOptionChosen as e:
        nuke.message(e.message)


def checkIfAnyImportOptionChosen(transformNode):
    for dataName in ["translate", "rotate", "scale", "skew"]:
        if transformNode["import" + dataName + "data"].getValue():
            return
    raise NoImportOptionChosen()


def setTransformDataForTransformNode(transformNode, tfData):
    if tfData.hasPositionData() and transformNode["importtranslatedata"].getValue():
        transformX = trackingDataConversion.tuplesToAnimationKeys(tfData.getPositionValues("x"))
        transformY = trackingDataConversion.tuplesToAnimationKeys(tfData.getPositionValues("y"))
        transformNode["translate"].clearAnimated()
        transformNode["translate"].setAnimated()
        transformNode["translate"].animation(0).addKey(transformX)
        transformNode["translate"].animation(1).addKey(transformY)

    if tfData.hasScaleData() and transformNode["importscaledata"].getValue():
        scaleX = trackingDataConversion.tuplesToAnimationKeys(tfData.getScaleValues("x"))
        scaleY = trackingDataConversion.tuplesToAnimationKeys(tfData.getScaleValues("y"))
        transformNode["scale"].clearAnimated()
        transformNode["scale"].setAnimated()
        transformNode["scale"].setValue(1, 1)
        # make sure the scale has two components, otherwise the next commands cause an error
        # see http://forums.thefoundry.co.uk/phpBB2/viewtopic.php?t=9614
        transformNode["scale"].animation(0).addKey(scaleX)
        transformNode["scale"].animation(1).addKey(scaleY)

    if tfData.hasRotationData() and transformNode["importrotatedata"].getValue():
        rotation = trackingDataConversion.tuplesToAnimationKeys(tfData.getRotationValues())
        transformNode["rotate"].clearAnimated()
        transformNode["rotate"].setAnimated()
        transformNode["rotate"].animation(0).addKey(rotation)

    if tfData.hasShearData() and transformNode["importskewdata"].getValue():
        shearX = trackingDataConversion.tuplesToAnimationKeys(tfData.getShearValues("x"))
        shearY = trackingDataConversion.tuplesToAnimationKeys(tfData.getShearValues("y"))
        transformNode["skewX"].clearAnimated()
        transformNode["skewX"].setAnimated()
        transformNode["skewX"].animation(0).addKey(shearX)
        transformNode["skewY"].clearAnimated()
        transformNode["skewY"].setAnimated()
        transformNode["skewY"].animation(0).addKey(shearY)

    transformNode["center"].clearAnimated()
    transformNode["center"].setAnimated()
    transformNode["center"].animation(0).setKey(0, 0)
    transformNode["center"].animation(1).setKey(0, 0)

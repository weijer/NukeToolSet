import nuke
import trackingDataConversion


def applyCornerPinDataToALlKnobs(cpData, knob1, knob2, knob3, knob4):
    applyCornerPinDataToKnob(cpData, knob1, 0)
    applyCornerPinDataToKnob(cpData, knob2, 1)
    applyCornerPinDataToKnob(cpData, knob3, 2)
    applyCornerPinDataToKnob(cpData, knob4, 3)


def applyCornerPinDataToKnob(cpData, knob, pointIndex):
    knob.setAnimated()
    xAnimation = trackingDataConversion.tuplesToAnimationKeys(cpData.getPointValues(pointIndex, 'x'))
    yAnimation = trackingDataConversion.tuplesToAnimationKeys(cpData.getPointValues(pointIndex, 'y'))
    knob.animation(0).clear()
    knob.animation(1).clear()
    knob.animation(0).addKey(xAnimation)
    knob.animation(1).addKey(yAnimation)


def addCornerPinKnob(parentNode, name, label):
    myKnob = nuke.XY_Knob(name, label)
    parentNode.addKnob(myKnob)
    myKnob.setTooltip("corner pin tracking data")


def addCornerPinUI(parentNode):
    loadDataKnob = nuke.PyScript_Knob("loadTrackingDataFromFile", "load tracking data from file")
    loadDataKnob.setTooltip("import mocha corner pin data from a file\n\nrequired format: Nuke Corner Pin (*.nk)")
    loadDataKnob.setCommand('import cornerPinData\ncornerPinData.loadCornerPinDataFromFile(nuke.thisNode() )')
    parentNode.addKnob(loadDataKnob)

    parentNode.addKnob(nuke.Text_Knob("divName", "", ""))

    addCornerPinKnob(parentNode, "pin1", "pin 1")
    addCornerPinKnob(parentNode, "pin2", "pin 2")
    addCornerPinKnob(parentNode, "pin3", "pin 3")
    addCornerPinKnob(parentNode, "pin4", "pin 4")

    pinTimeOffsetKnob = nuke.Array_Knob("pinTimeOffset", "Corner Pin Time Offset")
    pinTimeOffsetKnob.setTooltip("shift your tracking data if it does not start at the first frame")
    parentNode.addKnob(pinTimeOffsetKnob)


def createLinkedCornerPinOptions(cpNode, linkTargetNode):
    createLinkKnob(cpNode, linkTargetNode, 'filter', False)
    createLinkKnob(cpNode, linkTargetNode, 'clamp', False)
    createLinkKnob(cpNode, linkTargetNode, 'black_outside', False)
    createLinkKnob(cpNode, linkTargetNode, 'motionblur', True)
    createLinkKnob(cpNode, linkTargetNode, 'shutter', True)
    createLinkKnob(cpNode, linkTargetNode, 'shutteroffset', True)
    createLinkKnob(cpNode, linkTargetNode, 'shuttercustomoffset', False).setLabel("")


def createLinkKnob(srcNode, targetNode, propName, newLine):
    knob = nuke.Link_Knob(propName)
    knob.makeLink(srcNode.name(), propName)
    if newLine:
        knob.setFlag(nuke.STARTLINE)
    else:
        knob.clearFlag(nuke.STARTLINE)
    targetNode.addKnob(knob)
    return knob

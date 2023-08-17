import nuke
import re
import helper


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


toPrecompName = "stabilize"
fromPrecompName = "reverse stabilize"
reformateName = "reformat"


# LOAD FILE

def loadCornerPinData(parentNode):
    trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')

    trackingDataFile = open(trackingDataFilePath, mode='r')
    trackingData = trackingDataFile.read()
    trackingDataFile.close()

    # nuke.message(trackingData)

    # input of form "xFrame Value" like this "x0 472.276 x1 472.276 x2 472.276..."
    def parseKeyframeData(inputData):
        result = []
        simpleList = inputData.split()
        for i in range(1, len(simpleList), 2):
            key = simpleList[i - 1]
            value = float(simpleList[i])
            frameNumberWithX = key
            if frameNumberWithX[0] != "x":
                raise Error("invalid frame number in tracking data file: " + frameNumberWithX)
            frameNumber = float(frameNumberWithX[1:])  # skip first character
            result.append(nuke.AnimationKey(frameNumber, value))
        return result

    def parseCornerPoint(pointName):
        parseDataRegExp = re.compile(pointName + r"\s*{\s*{\s*curve\s*([^}]*)}\s*{\s*curve\s*([^}]*)}\s*}")
        trackingDataParse = parseDataRegExp.search(trackingData)
        if trackingDataParse is None:
            raise Error("invalid tracking data in file " + trackingDataFilePath)

        pointDataX = trackingDataParse.group(1)
        pointDataY = trackingDataParse.group(2)

        pointData = {'x': parseKeyframeData(pointDataX),
                     'y': parseKeyframeData(pointDataY)
                     }
        return pointData

    pin1KeyframeData = parseCornerPoint("to1")
    pin2KeyframeData = parseCornerPoint("to2")
    pin3KeyframeData = parseCornerPoint("to3")
    pin4KeyframeData = parseCornerPoint("to4")

    def setKeyframesForArrayKnob(knob, values):
        knob.setAnimated()
        knob.animation(0).addKey(values['x'])
        knob.animation(1).addKey(values['y'])

    setKeyframesForArrayKnob(parentNode['pin1'], pin1KeyframeData)
    setKeyframesForArrayKnob(parentNode['pin2'], pin2KeyframeData)
    setKeyframesForArrayKnob(parentNode['pin3'], pin3KeyframeData)
    setKeyframesForArrayKnob(parentNode['pin4'], pin4KeyframeData)


# CREATE RIG

toPrecomp = nuke.nodes.CornerPin2D(name=toPrecompName)
fromPrecomp = nuke.nodes.CornerPin2D(name=fromPrecompName)
reformat = nuke.nodes.Reformat(name=reformateName)

reformat.setInput(0, toPrecomp)
fromPrecomp.setInput(0, reformat)

if nuke.nodesSelected():
    toPrecomp.setInput(0, nuke.selectedNode())
helper.selectOnlyNode(toPrecomp)

fromPrecomp.setSelected(True)
reformat.setSelected(True)

precomp = nuke.collapseToGroup()
precomp.setName("Stabilized Grp")

precomp.addKnob(nuke.Tab_Knob("stabilizedgroup", "Stabilized Group"))


def addCornerPinKnob(parentNode, name, label):
    myKnob = nuke.XY_Knob(name, label)
    parentNode.addKnob(myKnob)
    myKnob.setTooltip("corner pin tracking data for the region you want to modify in the stabilized group")


addCornerPinKnob(precomp, "pin1", "Pin 1")
addCornerPinKnob(precomp, "pin2", "Pin 2")
addCornerPinKnob(precomp, "pin3", "Pin 3")
addCornerPinKnob(precomp, "pin4", "Pin 4")

projectWidth = precomp.width()
projectHeight = precomp.height()
precomp['pin1'].setValue(0, 0)  # set to [0,0]
precomp['pin1'].setValue(0, 1)
precomp['pin2'].setValue(projectWidth, 0)  # set to [width,0]
precomp['pin2'].setValue(0, 1)
precomp['pin3'].setValue(projectWidth, 0)  # set to [width,height]
precomp['pin3'].setValue(projectHeight, 1)
precomp['pin4'].setValue(0, 0)  # set to [0,height]
precomp['pin4'].setValue(projectHeight, 1)

loadDataKnob = nuke.PyScript_Knob("loadTrackingDataFromFile", "Load Trackingdata from File")
loadDataKnob.setTooltip("load the corner pin data from a mocha Nuke corner pin (*.nk) file")
loadDataKnob.setFlag(nuke.STARTLINE)
loadDataKnob.setCommand("loadCornerPinData(nuke.thisNode() )")
precomp.addKnob(loadDataKnob)

precomp.addKnob(nuke.Text_Knob("divName", "", ""))

pinTimeOffsetKnob = nuke.Array_Knob("pinTimeOffset", "Corner Pin Time Offset")
pinTimeOffsetKnob.setTooltip("shift your tracking data if it does not start at the first frame")
precomp.addKnob(pinTimeOffsetKnob)

precomp.addKnob(nuke.Text_Knob("divName", "", ""))


def createLinkKnob(propName, newLine):
    knob = nuke.Link_Knob(propName)
    knob.makeLink(fromPrecompName, propName)
    if newLine:
        knob.setFlag(nuke.STARTLINE)
    else:
        knob.clearFlag(nuke.STARTLINE)
    precomp.addKnob(knob)
    return knob


createLinkKnob('filter', False)
createLinkKnob('clamp', False)
createLinkKnob('black_outside', False)
createLinkKnob('motionblur', True)
createLinkKnob('shutter', True)
createLinkKnob('shutteroffset', True)
createLinkKnob('shuttercustomoffset', False).setLabel("")

fromPrecomp = precomp.node(fromPrecompName)
fromPrecomp['to1'].setExpression("parent.pin1.x(t+parent.pinTimeOffset)", 0)
fromPrecomp['to1'].setExpression("parent.pin1.y(t+parent.pinTimeOffset)", 1)
fromPrecomp['to2'].setExpression("parent.pin2.x(t+parent.pinTimeOffset)", 0)
fromPrecomp['to2'].setExpression("parent.pin2.y(t+parent.pinTimeOffset)", 1)
fromPrecomp['to3'].setExpression("parent.pin3.x(t+parent.pinTimeOffset)", 0)
fromPrecomp['to3'].setExpression("parent.pin3.y(t+parent.pinTimeOffset)", 1)
fromPrecomp['to4'].setExpression("parent.pin4.x(t+parent.pinTimeOffset)", 0)
fromPrecomp['to4'].setExpression("parent.pin4.y(t+parent.pinTimeOffset)", 1)

toPrecomp = precomp.node(toPrecompName)
toPrecomp['from1'].setExpression("parent.pin1.x(t+parent.pinTimeOffset)", 0)
toPrecomp['from1'].setExpression("parent.pin1.y(t+parent.pinTimeOffset)", 1)
toPrecomp['from2'].setExpression("parent.pin2.x(t+parent.pinTimeOffset)", 0)
toPrecomp['from2'].setExpression("parent.pin2.y(t+parent.pinTimeOffset)", 1)
toPrecomp['from3'].setExpression("parent.pin3.x(t+parent.pinTimeOffset)", 0)
toPrecomp['from3'].setExpression("parent.pin3.y(t+parent.pinTimeOffset)", 1)
toPrecomp['from4'].setExpression("parent.pin4.x(t+parent.pinTimeOffset)", 0)
toPrecomp['from4'].setExpression("parent.pin4.y(t+parent.pinTimeOffset)", 1)


def placeNodeBelowNode(node1, node2):
    node1.setXpos(node2.xpos())
    node1.setYpos(node2.ypos() + node2.screenHeight())


def placeNodeAboveNode(node1, node2):
    node1.setXpos(node2.xpos())
    node1.setYpos(node2.ypos() - node2.screenHeight())


def improveStabilizedGroup():
    placeNodeBelowNode(nuke.toNode(toPrecompName), nuke.toNode("Input1"))
    placeNodeBelowNode(nuke.toNode(reformateName), nuke.toNode(toPrecompName))
    placeNodeAboveNode(nuke.toNode(fromPrecompName), nuke.toNode("Output1"))


precomp.run(improveStabilizedGroup)

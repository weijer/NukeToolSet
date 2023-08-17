import nuke
import loadTrackingDataTab
import cornerPinData
import curvesHelper
import CornerPinToPerspectiveTransform


def createRotoPaintNodeMI():
    return createRotoOrRotoPaintNodeMI('RotoPaint')


def createRotoNodeMI():
    return createRotoOrRotoPaintNodeMI('Roto')


def createSplineWarpNodeMI():
    return createRotoOrRotoPaintNodeMI('SplineWarp3')


def createRotoOrRotoPaintNodeMI(nodeType):
    rotoPaintNode = nuke.createNode(nodeType)

    loadTrackingDataTab.addLoadTrackingDataUI(
        rotoPaintNode,
        "mochaimport.RotoPaintNodeMI.loadTransformMatrixFromFilePopup(nuke.thisNode())",
        "mochaimport.RotoPaintNodeMI.loadTransformMatrixFromFromClipboard(nuke.thisNode())")

    layers = curvesHelper.getLayersAsList(rotoPaintNode['curves'])
    layerNames = curvesHelper.layerListToLayerNameList(layers)
    layerChoiceKnob = nuke.Enumeration_Knob("trackingDataLayerMI", "apply to layer", layerNames)
    layerChoiceKnob.setTooltip("choose here to which layer the tracking data should be applied.")
    rotoPaintNode.addKnob(layerChoiceKnob)

    createReferenceFrameUI(rotoPaintNode)

    rotoPaintNode['label'].setValue('MochaImportPlus')

    return rotoPaintNode


def loadTransformMatrixFromFilePopup(rotoPaintNode):
    try:
        trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')
        if trackingDataFilePath is None:
            return
        trackingData = cornerPinData.CornerPinDataFromNukeCornerPinFile(trackingDataFilePath)
        setCornerPinDataForRotoPaintNode(rotoPaintNode, trackingData)

    except IOError as e:
        nuke.message(
            "Could not read file {0}:\n\nI/O error({1}): {2}"
            .format(trackingDataFilePath, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message(
            "Could not read file {0}:\n\nInvalid File Format: {1}"
            .format(trackingDataFilePath, e.message))


def loadTransformMatrixFromFromClipboard(rotoPaintNode):
    try:
        trackingData = cornerPinData.CornerPinDataFromClipboard()
        setCornerPinDataForRotoPaintNode(rotoPaintNode, trackingData)
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))


def setCornerPinDataForRotoPaintNode(rotoPaintNode, cpData, choosenLayerIndex=None, referenceFrame=None):
    curves = rotoPaintNode['curves']

    if choosenLayerIndex is None:
        choosenLayerIndex = int(rotoPaintNode['trackingDataLayerMI'].getValue())
    allLayers = curvesHelper.getLayersAsList(curves)
    layer = allLayers[choosenLayerIndex]

    if referenceFrame is None:
        referenceFrame = getReferenceFrame(rotoPaintNode)

    matrixData = CornerPinToPerspectiveTransform.cp2TransformMatrix(cpData, referenceFrame)
    matrixData.applyToCurvesLayer(layer)
    curves.changed()


def getReferenceFrame(node):
    if node['useCurrentFrameAsReferenceFrame'].getValue():
        return int(nuke.frame())
    else:
        return int(node['referenceFrameMI'].getValue())


def createReferenceFrameUI(node):
    referenceFrameKnob = nuke.Array_Knob("referenceFrameMI", "reference frame")
    referenceFrameKnob.setTooltip(
        "at this frame, the shapes will preserve their position when the tracking data is loaded.")
    node.addKnob(referenceFrameKnob)

    useCurrentFrameKnob = nuke.Boolean_Knob("useCurrentFrameAsReferenceFrame", "use current frame")
    useCurrentFrameKnob.setTooltip(
        "at this frame, the shapes will preserve their position when the tracking data is loaded.")
    useCurrentFrameKnob.setValue(True)
    node.addKnob(useCurrentFrameKnob)

    updateReferenceFrameUIEnabled(node)


def updateReferenceFrameUIEnabled(node):
    useCurrentFrameKnob = node['useCurrentFrameAsReferenceFrame']
    referenceFrameKnob = node['referenceFrameMI']

    if not useCurrentFrameKnob:
        return
    if not referenceFrameKnob:
        return

    isEnabled = not useCurrentFrameKnob.getValue()
    referenceFrameKnob.setEnabled(isEnabled)


def updateReferenceFrameUIEnabledCallback():
    node = nuke.thisNode()
    knob = nuke.thisKnob()
    if knob.name() == 'useCurrentFrameAsReferenceFrame':
        updateReferenceFrameUIEnabled(node)


def updateLayerChoiceKnobMICallback():
    node = nuke.thisNode()
    knob = nuke.thisKnob()
    if knob.name() == "curves":
        # avoid getting error messages on normal nodes that don't have this knob
        if node.knob('trackingDataLayerMI'):
            tdKnob = node['trackingDataLayerMI']
            layers = curvesHelper.getLayersAsList(knob)
            layerNames = curvesHelper.layerListToLayerNameList(layers)
            tdKnob.setValues(layerNames)


nuke.addKnobChanged(updateLayerChoiceKnobMICallback, nodeClass='RotoPaint')
nuke.addKnobChanged(updateLayerChoiceKnobMICallback, nodeClass='Roto')
nuke.addKnobChanged(updateLayerChoiceKnobMICallback, nodeClass='SplineWarp3')
nuke.addKnobChanged(updateReferenceFrameUIEnabledCallback, nodeClass='RotoPaint')
nuke.addKnobChanged(updateReferenceFrameUIEnabledCallback, nodeClass='Roto')
nuke.addKnobChanged(updateReferenceFrameUIEnabledCallback, nodeClass='GridWarp3')
nuke.addKnobChanged(updateReferenceFrameUIEnabledCallback, nodeClass='SplineWarp3')


#######################################

def createGridWarpNodeMI():
    gridWarpNode = nuke.createNode('GridWarp3')

    loadTrackingDataTab.addLoadTrackingDataUI(
        gridWarpNode,
        "mochaimport.RotoPaintNodeMI.loadTransformMatrixFromFilePopupGridWarp(nuke.thisNode())",
        "mochaimport.RotoPaintNodeMI.loadTransformMatrixFromFromClipboardGridWarp(nuke.thisNode())")
    createReferenceFrameUI(gridWarpNode)

    gridWarpNode['label'].setValue('MochaImportPlus')
    return gridWarpNode


def loadTransformMatrixFromFilePopupGridWarp(node):
    try:
        trackingDataFilePath = nuke.getFilename('Load Nuke Corner Pin Data from mocha', '*.nk')
        if trackingDataFilePath is None:
            return
        trackingData = cornerPinData.CornerPinDataFromNukeCornerPinFile(trackingDataFilePath)
        setCornerPinDataForMatrixToArrayKnob(node, trackingData, "source_grid_transform_matrix")

    except IOError as e:
        nuke.message(
            "Could not read file {0}:\n\nI/O error({1}): {2}"
            .format(trackingDataFilePath, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message(
            "Could not read file {0}:\n\nInvalid File Format: {1}"
            .format(trackingDataFilePath, e.message))


def loadTransformMatrixFromFromClipboardGridWarp(node):
    try:
        trackingData = cornerPinData.CornerPinDataFromClipboard()
        setCornerPinDataForMatrixToArrayKnob(node, trackingData, "source_grid_transform_matrix")
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))


def setCornerPinDataForMatrixToArrayKnob(node, cpData, knobName):
    referenceFrame = getReferenceFrame(node)

    matrixData = CornerPinToPerspectiveTransform.cp2TransformMatrix(cpData, referenceFrame)
    matrixData.applyToArrayKnob(node[knobName])

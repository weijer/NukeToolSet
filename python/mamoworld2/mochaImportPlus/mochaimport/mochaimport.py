"""
MAIN SCRIPT FILE
"""
import nuke
import cameraMI
import bakeGizmosMi
import cornerPinKnobs
import cornerPinData
import CornerPinToPerspectiveTransform
import helper
import nodeGraphHelper
import stabilizedPrecompNode
import trackerNodeMI
import transformNodeMI
import RotoPaintNodeMI
import transformData
# ! Gizmos require this unused import to be present. Do not delete this.

MiSettings_useGroupsInsteadOfGizmos = True


class MiUnsupportedNodeTypeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def createStabilizedView():
    """Creates a Stabilized View Rig """
    startPrecompNode = nuke.createNode('StartStabilized')
    placeholderTop = nuke.createNode('Dot', '', False)
    placeholderBottom = nuke.createNode('Dot', '', False)
    endPrecompNode = nuke.createNode('EndStabilized')

    if MiSettings_useGroupsInsteadOfGizmos:
        startPrecompNode = bakeGizmosMi.bakeStabilizedViewStart(startPrecompNode)
        endPrecompNode = bakeGizmosMi.bakeStabilizedViewEnd(endPrecompNode)

    startPrecompNode['tile_color'].setValue(
        int('%02x%02x%02x%02x' % (int(0.91 * 255), int(0.569 * 255), int(0 * 255), 255), 16))  # [0.91,0.569,0]
    endPrecompNode['tile_color'].setValue(
        int('%02x%02x%02x%02x' % (int(0.91 * 255), int(0.569 * 255), int(0 * 255), 255), 16))  # [0.91,0.569,0]

    endPrecompNode.connectInput(2, startPrecompNode)

    stabilizedPrecompNode.connectPrecompNodes(startPrecompNode, endPrecompNode)

    # width and height of the square formed by the 4 main nodes of the rig
    deltaX = 250
    deltaY = 250
    # border = 50

    # this should work, but doesn't since startPrecompNode.screenHeight() seems to return a wrong value...
    # nodeHeightCorrectionFactor = startPrecompNode.screenHeight()/2 - placeholderTop.screenHeight()/2
    nodeHeightCorrectionFactor = 7

    helper.selectOnlyNode(placeholderTop)

    placeholderBottom.setSelected(True)

    # Disabled backdrop code
    # stabilizeBackdrop = nuke.nodes.BackdropNode(xpos=startPrecompNode.xpos() + deltaX / 2,
    #                                             bdwidth=deltaX * 1.5,
    #                                             ypos=startPrecompNode.ypos() - border,
    #                                             bdheight=deltaY + 2 * border,
    #                                             tile_color=int(
    #                                                 '%02x%02x%02x%02x' % (
    #                                                     int(0.91 * 255), int(0.569 * 255), int(0 * 255), 255), 16),
    #                                             # [0.91,0.569,0]
    #                                             note_font_color=0xFFFFFF00,
    #                                             note_font_size=36,
    #                                             name='MochaImportPlus')
    #
    # stabilizeBackdrop['label'].setValue('Stabilized View+')

    placeholderTop.setXpos(startPrecompNode.xpos() + deltaX)
    placeholderTop.setYpos(startPrecompNode.ypos() + nodeHeightCorrectionFactor)
    placeholderBottom.setXpos(startPrecompNode.xpos() + deltaX)
    placeholderBottom.setYpos(startPrecompNode.ypos() + deltaY + nodeHeightCorrectionFactor)
    endPrecompNode.setXpos(startPrecompNode.xpos())
    endPrecompNode.setYpos(startPrecompNode.ypos() + deltaY)

    # Disabled backdrop code
    #     stabilizeBackdrop['help'].setValue("""
    # <h2>Basic Usage of Stabilized View Rig</h2>
    # <ol>
    # <li>From the MochaImportPlus menu, create the stabilized view rig consisting of the StartStabilized node, the EndStabilized node, and the Stabilized View Backdrop.</li>
    # <li>Load your mocha tracking data in the StartStabilized node.
    # <li>Do arbitrary manipulations in the Stabilized View by inserting new nodes inside the backdrop. All changes you do there in a stabilized setting will also be visible in your original perspective after the EndStabilized node.</li>
    # </ol>
    #
    # <h2>Lens Distortion</h2>
    # <p>If you've used the mocha Lens module to analyze the lens distortion of your clip, you need to do the following things to get an undistorted stabilized view and reapply the lens distortion to the final result:
    # <ul>
    # <li>make sure the mocha corner pin data you load into the StartStabilized node is exported from mocha Pro with the option 'Remove lens distortion'</li>
    # <li>as UndistMap input of the StartStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'undistort'.</li>
    # <li>as DistMap input of the EndStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</li>
    # </ul>""".replace('\n', '').replace('\r', ''))


def createCornerPin():
    """Creates a CornerPin with Lens Distortion node
    By default, a CornerPin with Lens Distortion is a group node. If mochaimport.setUseGizmos(True) has been called before,
    it will be a gizmo instead of a group.
    :returns: the created node
    """
    cpNode = nuke.createNode('CornerPinMI')
    cpNode['tile_color'].setValue(
        int('%02x%02x%02x%02x' % (int(0.91 * 255), int(0.569 * 255), 0 * 255, 255), 16))  # [0.91,0.569,0]

    if MiSettings_useGroupsInsteadOfGizmos:
        cpNode = bakeGizmosMi.bakeCornerPinMI(cpNode)

    return cpNode


def createTracker3Node():
    """Creates a Tracker+ (old) node
    A Tracker+ (old) node is a Tracker3 node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return trackerNodeMI.createTracker3NodeMI()


def createTracker4Node():
    """Creates a Tracker+ node
    A Tracker+ node is a Tracker4 node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return trackerNodeMI.createTracker4NodeMI()


def createTransformNodeMI():
    transformNodeMI.createTransformNodeMI()


def createRotoPaintNodeMI():
    """Creates a RotoPaint+ node
    A RotoPaint+ node is a RotoPaint node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return RotoPaintNodeMI.createRotoPaintNodeMI()


def createRotoNodeMI():
    """Creates a Roto+ node
    A Roto+ node is a Roto node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return RotoPaintNodeMI.createRotoNodeMI()


def createGridWarpNodeMI():
    """Creates a GridWarp+ node
    A GridWarp+ node is a GridWarp3 node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return RotoPaintNodeMI.createGridWarpNodeMI()


def createSplineWarpNodeMI():
    """Creates a SplineWarp+ node
     A SplineWarp+ node is a SplineWarp3 node that is extended with the ability to load mocha tracking data
    :returns: the created node
    """
    return RotoPaintNodeMI.createSplineWarpNodeMI()


def createCameraAndPointCloud(mochaFbxFilePath=None):
    """Creates a camera node and a point cloud node for a fbx file exported from mocha
    The function sets all options of the two nodes to interpret the fbx file from mocha properly.
    If None is given as mochaFbxFilePath, the function shows a open file dialog to choose an fbx file.
    """
    if mochaFbxFilePath is None:
        cameraMI.createCameraAndPointCloud()
    else:
        cameraMI.createMochaCameraFromFbxFile(mochaFbxFilePath)
        cameraMI.createMochaPointCloudFromFbxFile(mochaFbxFilePath)


def createCameraRig(mochaFbxFilePath=None):
    """Creates a mocha camera rig for a fbx file exported from mocha
    If None is given as mochaFbxFilePath, the function shows a open file dialog to choose an fbx file
    """
    if mochaFbxFilePath is None:
        cameraMI.createMochaCameraRig()
    else:
        cameraMI.createMochaCameraRigFromFbxFile(mochaFbxFilePath)


def showSettings():
    """Shows the settings dialog of MochaImportPlus"""
    nuke.message("Settings dialog is not implemented yet")


def setUseGizmos(value=True):
    """Force MochaImportPlus to use gizmos instead of groups for stabilized views and corner pins.
    Note that this breaks compatibility with machines where MochaImportPlus is not installed.
    """
    global MiSettings_useGroupsInsteadOfGizmos
    MiSettings_useGroupsInsteadOfGizmos = not value


def applyMochaDataToNode(node, cornerpinData, referenceFrame=1, layerIndex=0):
    """Applies mocha cornerpin data to a node
    the node can have any of the node types supported by MochaImportPlus.
    :param node: the node to which the mocha tracking data should be applied
    :param cornerpinData: mocha corner pin data represented as a string
    :param referenceFrame: at which frame the moved object should be unchanged
    (only for the node types that have this control in their MochaImportPlus tab)
    :param layerIndex: to which layer of the node the trackingdata is applied
    (optional, only for Roto, RotoPaint and SplineWarp nodes)
    """
    supportedNodeClasses = ['Transform', 'Tracker3', 'Tracker4', 'Group', 'GridWarp3', 'SplineWarp3',
                            'Roto', 'RotoPaint', 'CornerPinMI', 'StartStabilized']

    if node.Class() not in supportedNodeClasses:
        raise MiUnsupportedNodeTypeError("cannot apply mocha tracking data to node of class: " + node.Class())
    if node.Class() == 'Group' and (
            node.knob('pin1') is None
            or node.knob('pin2') is None
            or node.knob('pin3') is None
            or node.knob('pin4') is None):
        raise MiUnsupportedNodeTypeError(
            "Can only apply tracking data to groups, if they have the knobs 'pin1', 'pin2', 'pin3' and 'pin4'")

    cpData = cornerPinData.CornerPinDataFromNukeCornerPinText(cornerpinData)

    if node.Class() == 'Transform':
        tfData = transformData.TransformDataFromCornerPinData(cpData)
        transformNodeMI.setTransformDataForTransformNode(node, tfData)
    elif node.Class() == 'Tracker3':
        trackerNodeMI.setCornerPinDataForTracker3Node(node, cpData)
    elif node.Class() == 'Tracker4':
        trackerNodeMI.setCornerPinDataForTracker4Node(node, cpData)
    elif node.Class() in ['Group', 'CornerPinMI', 'StartStabilized']:
        cornerPinKnobs.applyCornerPinDataToALlKnobs(cpData,
                                                    node['pin1'],
                                                    node['pin2'],
                                                    node['pin3'],
                                                    node['pin4'])
    elif node.Class() == 'GridWarp3':
        matrixData = CornerPinToPerspectiveTransform.cp2TransformMatrix(cpData, referenceFrame)
        matrixData.applyToArrayKnob(node["source_grid_transform_matrix"])
    elif node.Class() in ['SplineWarp3', 'Roto', 'RotoPaint']:
        RotoPaintNodeMI.setCornerPinDataForRotoPaintNode(node, cpData, layerIndex, referenceFrame)


def OLDcreateCornerPin():
    cpNodeName = "corner pin"
    distortionMapSTMapNodeName = "apply distortion"
    distortionMapReadNodeName = "distortion map"

    cpNode = nuke.nodes.CornerPin2D(name=cpNodeName)
    distortionMapSTMapNode = nuke.nodes.STMap(name=distortionMapSTMapNodeName, disable=True)
    distortionMapReadNode = nuke.nodes.Read(name=distortionMapReadNodeName)

    if nuke.nodesSelected():
        father = nuke.selectedNode()
        nodeGraphHelper.moveChildren(father, distortionMapSTMapNode)
        cpNode.setInput(0, father)

    distortionMapSTMapNode.setInput(0, cpNode)
    distortionMapSTMapNode.setInput(1, distortionMapReadNode)

    helper.selectOnlyNode(cpNode)
    distortionMapSTMapNode.setSelected(True)
    distortionMapReadNode.setSelected(True)

    precomp = nuke.collapseToGroup()
    precomp.setName("corner pin MI")

    cpNode = precomp.node(cpNodeName)

    cornerPinKnobs.addCornerPinUI(precomp)
    precomp.addKnob(nuke.Text_Knob("divName", "", ""))
    cornerPinKnobs.createLinkedCornerPinOptions(cpNode, precomp)

    cpNode['to1'].setExpression("parent.pin1.x(t+parent.pinTimeOffset)", 0)
    cpNode['to1'].setExpression("parent.pin1.y(t+parent.pinTimeOffset)", 1)
    cpNode['to2'].setExpression("parent.pin2.x(t+parent.pinTimeOffset)", 0)
    cpNode['to2'].setExpression("parent.pin2.y(t+parent.pinTimeOffset)", 1)
    cpNode['to3'].setExpression("parent.pin3.x(t+parent.pinTimeOffset)", 0)
    cpNode['to3'].setExpression("parent.pin3.y(t+parent.pinTimeOffset)", 1)
    cpNode['to4'].setExpression("parent.pin4.x(t+parent.pinTimeOffset)", 0)
    cpNode['to4'].setExpression("parent.pin4.y(t+parent.pinTimeOffset)", 1)

    nodeGraphHelper.autoPlaceGroup(precomp)

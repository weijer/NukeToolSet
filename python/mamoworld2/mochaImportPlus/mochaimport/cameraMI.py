import nuke
import os
import helper
import nodeGraphPlacement


def createCameraAndPointCloud():
    fbxFilePath = nuke.getFilename('Load from mocha FBX 6.1.0 3D Data for Nuke 6.3v7', '*.fbx')
    if fbxFilePath is None or (not os.path.isfile(fbxFilePath)):
        return
    if not fbxFilePath.lower().endswith('.fbx'):
        nuke.message(
            "filename must end with .fbx\nPlease choose a "
            "file exported with mocha Pro's camera module choosing the "
            "format named 'FBX 6.1.0 3D Data for Nuke 6..3v7 (*.fbx)'")
        return
    createMochaCameraFromFbxFile(fbxFilePath)
    createMochaPointCloudFromFbxFile(fbxFilePath)


def createMochaCameraFromFbxFile(fbxFilePath):
    camera = nuke.createNode('Camera2', 'file "%s" read_from_file True' % fbxFilePath)
    camera['fbx_node_name'].setValue('MochaCameraNode')

    label = labelFromPath(fbxFilePath)
    camera['label'].setValue(label)

    return camera


def createMochaPointCloudFromFbxFile(fbxFilePath):
    geo = nuke.createNode('ReadGeo2', 'file "%s"' % fbxFilePath)
    geo['object_type'].setValue('Point Cloud')
    geo['label'].setValue('MochaImportPlus')
    return geo


def createMochaCameraRig():
    fbxFilePath = nuke.getFilename('Load from mocha FBX 6.1.0 3D Data for Nuke 6.3v7', '*.fbx')
    if fbxFilePath is None or (not os.path.isfile(fbxFilePath)):
        return
    if not fbxFilePath.lower().endswith('.fbx'):
        nuke.message(
            "filename must end with .fbx\nPlease choose a file exported with mocha Pro's "
            "camera module choosing the format named 'FBX 6.1.0 3D "
            "Data for Nuke 6..3v7 (*.fbx)'")
        return

    createMochaCameraRigFromFbxFile(fbxFilePath)


def createMochaCameraRigFromFbxFile(fbxFilePath):
    selectedNode = False
    if nuke.nodesSelected():
        selectedNode = nuke.selectedNode()

    cam = createMochaCameraFromFbxFile(fbxFilePath)
    pointCloud = createMochaPointCloudFromFbxFile(fbxFilePath)
    scene = nuke.createNode('Scene')
    render = nuke.createNode('ScanlineRender')
    worldTransform = nuke.createNode('TransformGeo')
    worldAxis = nuke.createNode('Axis2')

    scene.setInput(0, worldTransform)
    scene.setInput(1, cam)
    worldTransform.setInput(0, pointCloud)
    worldTransform.setInput(1, worldAxis)
    cam.setInput(0, worldAxis)
    render.setInput(1, scene)
    render.setInput(2, cam)

    placer = nodeGraphPlacement.GridPlacer()

    if selectedNode:
        render.setInput(0, selectedNode)
        placer.placeNodeRelativeToNode(cam, selectedNode, 2, 0)

    placer.placeNodeRelativeToNode(scene, cam, -1, 0)
    placer.placeNodeRelativeToNode(render, cam, -1, 1)
    placer.placeNodeRelativeToNode(worldTransform, cam, -1, -1)
    placer.placeNodeRelativeToNode(worldAxis, cam, 0, -1)
    placer.placeNodeRelativeToNode(pointCloud, cam, -2, -1)

    pointCloud.setName("PointCloud")
    worldAxis['label'].setValue("OrientWorld")

    pointCloud['help'].setValue(
        "renders the point cloud imported from the mocha "
        "camera track. Each tracked layer contributes 5 points "
        "(four corners + center of surface rectangle)")
    cam['help'].setValue("camera imported from mocha camera track")
    worldAxis['help'].setValue(
        "use this node to orient the camera track in your scene as "
        "desired (e.g. make the ground plane horizontal etc...)")
    worldTransform['help'].setValue(
        "applies your world transformations from node " + worldAxis.name() + " to the point cloud")

    # backdrop
    rigNodes = [cam, pointCloud, scene, render, worldTransform, worldAxis]
    helper.selectOnlyNode(cam)
    for node in rigNodes:
        node.setSelected(True)
    backdrop = mamoBackDrop()

    backdrop['label'].setValue('camera rig')
    rigNodes.append(backdrop)

    # this also solves some issue that the help texts are not updated until the control panels are closed and reopened
    for node in rigNodes:
        node.hideControlPanel()


def labelFromPath(path):
    filename = os.path.basename(path)
    label = filename + '\nMochaImportPlus'
    # todo remove everything from the path except the filename and maybe time to some maximum length

    return label


def mamoBackDrop():
    selNodes = nuke.selectedNodes()
    if not selNodes:
        return nuke.nodes.BackdropNode(tile_color=int('%02x%02x%02x%02x' % (0.91 * 255, 0.569 * 255, 0 * 255, 255), 16),
                                       # [0.91,0.569,0]
                                       note_font_color=0xFFFFFF00,
                                       note_font_size=36,
                                       name='MochaImportPlus')
    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in selNodes])
    bdY = min([node.ypos() for node in selNodes])
    bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

    # Expand the bounds to leave a little border.
    # Elements are offsets for left, top, right and bottom edges respectively
    left, top, right, bottom = (-10, -80, 10, 10)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    n = nuke.nodes.BackdropNode(xpos=bdX, bdwidth=bdW, ypos=bdY, bdheight=bdH,
                                tile_color=int('%02x%02x%02x%02x' % (0.91 * 255, 0.569 * 255, 0 * 255, 255), 16),
                                # [0.91,0.569,0]
                                note_font_color=0xFFFFFF00,
                                note_font_size=36,
                                name='MochaImportPlus')

    n['selected'].setValue(True)
    for node in selNodes:
        node['selected'].setValue(True)
    return n

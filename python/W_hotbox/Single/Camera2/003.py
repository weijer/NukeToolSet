#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Projection Setup
#
#----------------------------------------------------------------------------------------------------------

def deselectAll():
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()
deselectAll()

for cameraNode in selection:
    cameraNode.knob('selected').setValue(True)

    #creation
    dotNode1 = nuke.createNode('Dot', inpanel=False)

    dotNode2 = nuke.createNode('Dot', inpanel=False)
    scanlineRenderNode = nuke.createNode('ScanlineRender', inpanel=False)
    deselectAll()

    dotNode1.knob('selected').setValue(True)
    dotNode3 = nuke.createNode('Dot', inpanel=False)
    frameHoldNode = nuke.createNode('FrameHold', inpanel=False)
    dotNode4 = nuke.createNode('Dot', inpanel=False)
    project3DNode = nuke.createNode('Project3D', inpanel=False)
    sphereNode = nuke.createNode('Sphere', inpanel=False)

    #connections
    dotNode2.setInput(0,dotNode1)
    scanlineRenderNode.setInput(1,sphereNode)

	#values
    project3DNode.knob('crop').setValue(False)
    camTrans = cameraNode.knob('translate').value()
    sphereNode.knob('translate').setValue(camTrans)
    sphereNode.knob('uniform_scale').setValue(1000)
    frameHoldNode.knob('first_frame').setValue(nuke.frame())

    #placement

    camXpos = cameraNode.xpos()
    camYpos = cameraNode.ypos()

    dotNode3.setXYpos(camXpos--118, camYpos--109)
    dotNode1.setXYpos(camXpos--24, camYpos--109)
    frameHoldNode.setXYpos(camXpos--84, camYpos--164)
    dotNode2.setXYpos(camXpos--24, camYpos--410)
    project3DNode.setXYpos(camXpos--264, camYpos--231)
    dotNode4.setXYpos(camXpos--118, camYpos--235)
    sphereNode.setXYpos(camXpos--264, camYpos--313)
    scanlineRenderNode.setXYpos(camXpos--264, camYpos--406)

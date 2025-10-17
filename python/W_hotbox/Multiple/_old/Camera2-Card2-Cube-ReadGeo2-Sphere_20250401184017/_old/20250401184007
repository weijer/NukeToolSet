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

if len(selection) == 2:

    
    for node in selection:
        if node.Class() == 'Camera2':
            cameraNode = node
        else:
            geoNode = node
    
    
    deselectAll()
    
    cameraNode.knob('selected').setValue(True)
    
    #creation
    dotNode1 = nuke.createNode('Dot')
    
    dotNode2 = nuke.createNode('Dot')
    scanlineRenderNode = nuke.createNode('ScanlineRender')
    deselectAll()
    
    dotNode1.knob('selected').setValue(True)
    dotNode3 = nuke.createNode('Dot')
    frameHoldNode = nuke.createNode('FrameHold') 
    dotNode4 = nuke.createNode('Dot')
    project3DNode = nuke.createNode('Project3D')
    
    
    #connections
    geoNode.setInput(0,project3DNode)
    dotNode2.setInput(0,dotNode1)
    scanlineRenderNode.setInput(1,geoNode)
    
    #values
    project3DNode.knob('crop').setValue(False)
    camTrans = cameraNode.knob('translate').value()
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
    geoNode.setXYpos(camXpos--264, camYpos--313)
    scanlineRenderNode.setXYpos(camXpos--264, camYpos--406)
    
    deselectAll()

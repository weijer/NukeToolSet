#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert to ChannelMerge
#
#----------------------------------------------------------------------------------------------------------

nodeClass = 'ChannelMerge'

selection = nuke.selectedNodes()

for node in selection:

    #check whether original node has a mask input
    maskInput = None
    for knob in node.knobs().keys():
        if knob.startswith('maskChannel'):
            maskInput = node.minInputs() - 1

    #save inputs
    inputs = {}

    counter = 0
    for i in range(node.maxInputs()):
        inputNode =  node.input(i)
        if inputNode != None:
            if i == maskInput:
                inputs['MASK'] = inputNode
                counter -= 1
            else:
                inputs[counter] = inputNode
        counter += 1
    
    #save position
    position = [node.xpos(),node.ypos()]

    #make sure no nodes are selected
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

    #create new node
    newNode = nuke.createNode(nodeClass, inpanel = False)
            
    newNode.knob('selected').setValue(False)

    #check whether new node has a mask input
    maskInput = None
    for knob in newNode.knobs().keys():
        if knob.startswith('maskChannel'):
            maskInput = newNode.minInputs() - 1

    #reconnect inputs
    counter = 0
    for i in range(newNode.maxInputs()):
        if i == maskInput:
            try:
                newNode.setInput(maskInput,inputs['MASK'])
            except:
                pass
        else:
            try:
                newNode.setInput(i,inputs[counter])
            except:
                pass
            counter += 1
    #reconnect outputs
    node.knob('selected').setValue(True)
    tmpDotNode = nuke.createNode('Dot')
    node.knob('selected').setValue(False)
    
    tmpDotNode.setInput(0,newNode)
    nuke.delete(tmpDotNode)
        
    #delete original
    nuke.delete(node)
        
    newNode.setXpos(position[0])
    newNode.setYpos(position[1])


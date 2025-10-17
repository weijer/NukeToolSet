#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Reorder inputs
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():

    inputs = []
    
    for i in range(node.inputs()):
        if node.input(i) != None:
            inputs.append(node.input(i))
            node.setInput(i,None)
    
    for index, inputNode in enumerate(inputs):
        node.setInput(index, inputNode)
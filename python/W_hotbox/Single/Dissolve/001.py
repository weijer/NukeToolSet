#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Dissolve between FrameHolds
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():

    inputDict = {int(node.knob('first_frame').value()):index for index, node in enumerate(nuke.dependencies(nuke.selectedNode())) if node.Class() == 'FrameHold'}
    
    i.knob('which').setAnimated(0)
    
    for inputNode in sorted(inputDict.keys()):
        i.knob('which').setValueAt(inputDict[inputNode],inputNode)
#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Card
#
#----------------------------------------------------------------------------------------------------------

def emptySelection():
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection()

for i in selection:
    cardNode = nuke.createNode('Card2')
    cardNode.knob('translate').setValue(i.knob('point3d').value())
    emptySelection()
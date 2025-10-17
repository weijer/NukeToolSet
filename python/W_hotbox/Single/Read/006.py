#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Overscan
#
#----------------------------------------------------------------------------------------------------------

def emptySelection():
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

for i in nuke.selectedNodes():
	emptySelection()
	i.knob('selected').setValue(True)
	reformatNode = nuke.createNode('Reformat')
	reformatNode.knob('resize').setValue('none')
	reformatNode.knob('pbb').setValue(True)
	reformatNode.knob('label').setValue('OVERSCAN')
emptySelection()
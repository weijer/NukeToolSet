#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Premult
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

for i in selection:
	emptySelection(selection)
	i.knob('selected').setValue(True)
	nuke.createNode('Premult', inpanel = False)
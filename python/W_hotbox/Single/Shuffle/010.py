#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: New Shuffle
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

newList = []

def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

for i in selection:
	emptySelection(selection)
	i.knob('selected').setValue(True)
	newNode = nuke.createNode('Shuffle', inpanel = False)
	newList.append(newNode)

emptySelection(selection)
for i in newList:
	i.knob('selected').setValue(True)
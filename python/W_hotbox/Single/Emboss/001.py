#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Grade
#
#----------------------------------------------------------------------------------------------------------

def emptySelection():
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

for i in nuke.selectedNodes():
    emptySelection()
    i.knob('selected').setValue(True)
    gradeNode = nuke.createNode('Grade')
    gradeNode.knob('add').setValue(-.5)
emptySelection()
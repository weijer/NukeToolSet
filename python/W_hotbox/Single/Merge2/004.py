#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: New Mask
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    rotoNode = nuke.createNode('Roto')
    dotNode = nuke.createNode('Dot', inpanel = False)
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]

    dotNode.setXpos(postion[0]+310-dotNode.screenWidth()/2)
    dotNode.setYpos(postion[1]-dotNode.screenHeight()/2)

    rotoNode.setXpos(postion[0]+310-rotoNode.screenWidth()/2)
    rotoNode.setYpos(postion[1]-100+rotoNode.screenHeight()/2)

    i.setInput(2,dotNode)
    emptySelection(selection)
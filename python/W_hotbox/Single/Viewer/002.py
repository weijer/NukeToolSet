#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: place Viewer
#
#----------------------------------------------------------------------------------------------------------

posDict = {i.ypos()+i.screenHeight():i.xpos() for i in nuke.allNodes('Write')}

ypos = max(posDict.keys())
xpos = posDict[ypos]

for index, node in enumerate(nuke.selectedNodes()):
    node.setXpos(xpos)
    node.setYpos(ypos + 100*(index+1))
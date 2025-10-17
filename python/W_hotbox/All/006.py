#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mirror
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()
allXpos = [i.xpos()+(i.screenWidth()/2) for i in selection]
minXpos = min(allXpos)
maxXpos = max(allXpos)

for index, i in enumerate(selection):
    i.setXpos((maxXpos - allXpos[index] + minXpos)-(i.screenWidth()/2))
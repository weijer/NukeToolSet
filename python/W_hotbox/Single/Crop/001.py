#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: To Format
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    inputNode = i.input(0)
    i.knob('box').setValue((0,0,inputNode.width(),inputNode.height()))
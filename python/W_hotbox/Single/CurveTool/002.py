#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Crop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    cropNode = nuke.createNode('Crop')
    cropNode.knob('box').fromScript(i.knob('autocropdata').toScript())
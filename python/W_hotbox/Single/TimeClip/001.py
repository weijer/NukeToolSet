#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Start on current frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('first').setValue(nuke.frame())

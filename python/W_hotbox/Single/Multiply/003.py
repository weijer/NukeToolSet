#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Animated
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	curValue = i.knob('value').value()
	i.knob('value').setAnimated()
	curValue = i.knob('value').setValue(curValue)
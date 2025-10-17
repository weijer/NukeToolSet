#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: hide Viewer lines
#
#----------------------------------------------------------------------------------------------------------

value = None

for i in nuke.allNodes('Viewer'):
	if value == None:
		value = i.knob('hide_input').value()
	i.knob('hide_input').setValue(1-value)
#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: +1
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('time_offset').setValue(i.knob('time_offset').value()+1)
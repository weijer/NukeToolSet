#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Previous Input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('which').setValue( max( (i.knob('which').value() - 1),  0) )
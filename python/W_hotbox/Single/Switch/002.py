#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Next Input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('which').setValue( min( (i.knob('which').value() + 1),  (i.inputs() - 1)) )
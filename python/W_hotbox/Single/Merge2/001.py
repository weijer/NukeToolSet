#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Max
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('output').setValue('rgb')
	i.knob('operation').setValue('max')
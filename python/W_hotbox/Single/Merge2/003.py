#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Plus
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('output').setValue('rgb')
	i.knob('operation').setValue('plus')
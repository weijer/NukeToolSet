#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Over/Under
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('output').setValue('rgba')
	if i.knob('operation').value() == 'over':
	    i.knob('operation').setValue('under')
	else:
	    i.knob('operation').setValue('over')
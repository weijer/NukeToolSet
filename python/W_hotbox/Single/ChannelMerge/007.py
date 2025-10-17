#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Union
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('operation').setValue('union')
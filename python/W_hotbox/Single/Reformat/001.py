#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Overscan
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('resize').setValue('none')
	i.knob('pbb').setValue(True)
	i.knob('label').setValue('OVERSCAN')
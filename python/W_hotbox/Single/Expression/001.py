#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Combine RGB
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('expr3').setValue('clamp(r+g+b)')
	i.knob('label').setValue('RGB to Alpha')
	i.knob('tile_color').setValue(4278124287)
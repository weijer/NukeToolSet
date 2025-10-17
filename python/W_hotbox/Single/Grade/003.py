#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Clamp
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('black_clamp').setValue(1-i.knob('black_clamp').value())
	i.knob('white_clamp').setValue(i.knob('black_clamp').value())
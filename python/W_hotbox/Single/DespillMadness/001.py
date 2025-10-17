#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Blue/Green
#
#----------------------------------------------------------------------------------------------------------

colors = [10485759,11339775]

for i in nuke.selectedNodes():
	curValue = int(i.knob('screenType').getValue())
	i.knob('screenType').setValue(1-curValue)
	i.knob('tile_color').setValue(colors[curValue])
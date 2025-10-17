#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set to Range
#
#----------------------------------------------------------------------------------------------------------

firstFrame = int(nuke.Root().knob('first_frame').value())
lastFrame = int(nuke.Root().knob('last_frame').value())
nuke.frame(lastFrame)
for i in nuke.selectedNodes():
	i.knob('framesbehind').setValue(lastFrame-firstFrame)
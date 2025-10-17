#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Render Camera
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('projection_mode').setValue('render camera')
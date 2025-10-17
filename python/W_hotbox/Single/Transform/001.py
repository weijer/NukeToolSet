#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Invert
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	invertKnob = i.knob('invert_matrix')
	invertKnob.setValue(1-int(invertKnob.value()))
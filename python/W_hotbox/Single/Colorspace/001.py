#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Swap
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    inKnob = i.knob('colorspace_in')
    outKnob = i.knob('colorspace_out')

    inValue = inKnob.value()
    outValue = outKnob.value()

    inKnob.setValue(outValue)
    outKnob.setValue(inValue)
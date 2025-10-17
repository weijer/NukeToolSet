#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Swap
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    inKnob = i.knob('in_colorspace')
    outKnob = i.knob('out_colorspace')

    inValue = inKnob.value()
    outValue = outKnob.value()

    inKnob.setValue(outValue)
    outKnob.setValue(inValue)
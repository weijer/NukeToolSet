#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Invert
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    p0Knob = i.knob('p0')
    p1Knob = i.knob('p1')

    p0Value = p0Knob.value()
    p1Value = p1Knob.value()

    p0Knob.setValue(p1Value)
    p1Knob.setValue(p0Value)
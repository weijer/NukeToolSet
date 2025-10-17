#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Toggle Invert Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    maskKnob = i.knob('invert_mask')
    if maskKnob == None:
        maskKnob = i.knob('invertMask')
    if maskKnob != None:
        maskKnob.setValue(1-maskKnob.value())
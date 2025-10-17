#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Pivot
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    pivotValues = [0,0,0]
    i.knob('orientation').value()
    for index, axis in enumerate('XYZ'):
        value = 0
        if axis in i.knob('orientation').value():
            value = -.5
        i.knob('pivot').setValue(value,index)
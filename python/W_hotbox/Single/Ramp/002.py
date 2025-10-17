#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Vertically
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    newPoint = (i.knob('p0').value()[1] + i.knob('p1').value()[1]) / 2

    i.knob('p0').setValue(newPoint,1)
    i.knob('p1').setValue(newPoint,1)
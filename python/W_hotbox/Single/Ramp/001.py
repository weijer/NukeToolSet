#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Horizontally
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    newPoint = (i.knob('p0').value()[0] + i.knob('p1').value()[0]) / 2

    i.knob('p0').setValue(newPoint,0)
    i.knob('p1').setValue(newPoint,0)
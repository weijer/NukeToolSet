#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Ground Pivot
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('translate').setValue((-1*(i.knob('pivot').value()[1])),1)

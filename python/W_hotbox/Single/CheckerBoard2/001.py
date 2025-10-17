#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Remove Centerline
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('centerlinewidth').setValue(0)
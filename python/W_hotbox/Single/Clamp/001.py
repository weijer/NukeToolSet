#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Toggle Maximum
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('maximum_enable').setValue(1-i.knob('maximum_enable').value())
#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Toggle Minimum
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('minimum_enable').setValue(1-i.knob('minimum_enable').value())
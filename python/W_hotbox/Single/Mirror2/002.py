#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Flop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('flop').setValue(1-i.knob('flop').value())
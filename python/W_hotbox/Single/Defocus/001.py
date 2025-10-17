#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Toggle Anamorphic
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('ratio').setValue(1.5-i.knob('ratio').value())

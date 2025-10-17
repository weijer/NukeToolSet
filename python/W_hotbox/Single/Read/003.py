#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Reload
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    nuke.Script_Knob.execute(i.knob('reload'))
#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: AutoCrop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('operation').setValue('Auto Crop')
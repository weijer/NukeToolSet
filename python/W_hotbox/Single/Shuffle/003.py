#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Red
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('in').setValue('rgba')
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('red')

    i.knob('tile_color').setValue(3204448511)
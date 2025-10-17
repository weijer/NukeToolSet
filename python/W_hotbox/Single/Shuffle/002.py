#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Blue
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('in').setValue('rgba')
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('blue')

    i.knob('tile_color').setValue(4177919)
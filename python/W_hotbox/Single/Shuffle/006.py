#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: pWorld
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if 'pWorld' in nuke.channels():
        i.knob('in').setValue('pWorld')
    else:
        i.knob('in').setValue('P')

    i.knob('tile_color').setValue(2130739199)
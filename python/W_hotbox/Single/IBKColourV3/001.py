#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Blue/Green
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('screen_type').value() == ('blue'):
        i.knob('screen_type').setValue('green')
        i.knob('tile_color').setValue(10027008)
    else:
        i.knob('screen_type').setValue('blue')
        i.knob('tile_color').setValue(3407871)
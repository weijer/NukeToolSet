#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Blue/Green
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('st').value() == ('C-blue'):
        i.knob('st').setValue('C-green')
        i.knob('tile_color').setValue(10027008)
    else:
        i.knob('st').setValue('C-blue')
        i.knob('tile_color').setValue(3407871)
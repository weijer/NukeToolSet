#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: rgb/rgba
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('output').value() == 'rgb':
        i.knob('output').setValue('rgba')
    else:
        i.knob('output').setValue('rgb')
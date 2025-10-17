#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: All/rgb
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('channels').value() != 'rgb':
        i.knob('channels').setValue('rgb')
    else:
        i.knob('channels').setValue('all')
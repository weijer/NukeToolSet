#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha/rgba/All
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('channels').value() == 'alpha':
        i.knob('channels').setValue('rgba')
    elif i.knob('channels').value() == 'rgba':
        i.knob('channels').setValue('all')
    else:
        i.knob('channels').setValue('alpha')
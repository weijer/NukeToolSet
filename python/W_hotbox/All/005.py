#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Paste to Selection
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

for i in selection:
    i.knob('selected').setValue('False')

for i in selection:
    i.knob('selected').setValue('True')
    nuke.nodePaste('%clipboard%')
    i.knob('selected').setValue('False')

for i in selection:
    i.knob('selected').setValue('True')
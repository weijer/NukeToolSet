#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: BBox Union/B
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNo des():
    if i.knob('bbox'). value() == 'union':
        i.knob('bbox'). setValue('B')
    else:
        i.knob('bbox').setValue('union')
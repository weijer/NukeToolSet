#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set To BBox
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    for index, axis in enumerate(['x','y','r','t']):
        i.knob('ROI').setExpression('input.bbox.%s'%axis,index)
#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Center
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    centerKnob = i.knob('center')

    centerKnob.setExpression('(input.bbox.r+input.bbox.x)/2',0)
    centerKnob.setExpression('(input.bbox.t+input.bbox.y)/2',1)
    
    centerKnob.clearAnimated()
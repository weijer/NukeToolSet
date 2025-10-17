#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Image Aspect
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    inputNode = i.input(0)
        
    if inputNode != None:
        i.knob('image_aspect').setValue(False)
        width = float(inputNode.width())
        height = float(inputNode.height())
    
        if width > height:
            aspect = width/height
            i.knob('scaling').setValue(aspect,0)
        else:
            aspect = height/width
            i.knob('scaling').setValue(aspect,1)

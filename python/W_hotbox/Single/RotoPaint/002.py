#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set LifeTime to All
#
#----------------------------------------------------------------------------------------------------------

#modified version of code found on the fourms
#http://community.thefoundry.co.uk/discussion/topic.aspx?f=190&t=102599

strokes = []

def getStrokes(layer):
    global strokes
    for element in layer:
        if isinstance(element, nuke.rotopaint.Layer):
            getStrokes(element)
        elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
            strokes.append(element)
    return strokes

for i in nuke.selectedNodes():
    curvesKnob = i.knob('curves')

    strokes = getStrokes(curvesKnob.rootLayer)

    for element in strokes:
        attrs = element.getAttributes()

        if 'ltt' in attrs:
            attrs.remove('ltt')
            attrs.add('ltt', 0)
        curvesKnob.changed()

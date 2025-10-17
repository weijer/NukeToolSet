#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert to Axis
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

for transformGeoNode in selection:

    #deselect all nodes
    for node in selection:
        node.knob('selected').setValue(False)
    
    axisNode = nuke.createNode('Axis')
        
    #resote settings
    ignoreKnobs = ['xpos','ypos','name','tile_color']

    for i in sorted(transformGeoNode.knobs().keys()):
        if i not in ignoreKnobs:
			try:
				axisNode.knob(i).setValue(transformGeoNode.knob(i).value())
			except:
				pass
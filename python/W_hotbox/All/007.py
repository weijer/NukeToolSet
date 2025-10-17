#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Viewer Input
#
#----------------------------------------------------------------------------------------------------------

node = nuke.activeViewer().node()

curNodeName = nuke.selectedNode().name()

if node.knob('input_process_node').value() == curNodeName:
	node.knob('input_process').setValue(1-node.knob('input_process').value())
else:
	node.knob('input_process_node').setValue(nuke.selectedNode().name())
	node.knob('input_process').setValue(True)
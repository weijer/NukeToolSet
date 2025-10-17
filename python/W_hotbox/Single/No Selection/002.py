#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Viewer Input Properties
#
#----------------------------------------------------------------------------------------------------------

viewerNode = nuke.activeViewer().node()
ipNode = nuke.toNode(viewerNode.knob('input_process_node').value())
nuke.show(ipNode)
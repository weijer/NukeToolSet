# node.selectOnly() does not work for NUKE 7.0v5 or older
# hence, we use this function instead
import nuke


def selectOnlyNode(myNode):
    for n in nuke.selectedNodes():
        n.setSelected(False)
    myNode.setSelected(True)

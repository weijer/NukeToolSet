import nuke


def moveChildren(fromNode, toNode):
    """ children of fromNode become children of toNode"""
    for node in fromNode.dependent(nuke.INPUTS):
        for i in range(0, node.inputs()):
            if node.input(i) == fromNode:
                node.setInput(i, toNode)


def autoPlaceGroup(groupNode):
    """run automatic layout on entire node graph of the group"""
    groupNode.begin()
    autoPlaceAllNodes()
    groupNode.end()


def autoPlaceAllNodes():
    """run automatic layout on all nodes"""
    for n in nuke.allNodes():
        n.autoplace()

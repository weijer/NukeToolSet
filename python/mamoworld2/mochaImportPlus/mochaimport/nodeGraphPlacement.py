import nuke


def placeNodesWithoutOverlapNicely(nodeList):
    for n in nodeList:
        n.autoplace()
    for n in nodeList:
        nuke.autoplaceSnap(n)


class GridPlacer(object):
    """places nodes in a regular grid distance relative to each other"""

    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.setGridSize(140, 120)

    def setGridSize(self, stepSizeX, stepSizeY):
        self.dx = stepSizeX
        self.dy = stepSizeY

    def placeNodeRelativeToNode(self, nodeToPlace, nodeReference, x, y):
        """places nodeToPlace x (y) grid steps away from nodeReference in x (y) direction"""
        sizeDifferenceX = nodeReference.screenWidth() - nodeToPlace.screenWidth()
        sizeDifferenceY = nodeReference.screenHeight() - nodeToPlace.screenHeight()
        nodeToPlace.setXpos(nodeReference.xpos() + x * self.dx + sizeDifferenceX / 2)
        nodeToPlace.setYpos(nodeReference.ypos() + y * self.dy + sizeDifferenceY / 2)

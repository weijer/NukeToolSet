import nuke


def tuplesToAnimationKeys(tupleList):
    # return map(lambda (x,y): nuke.AnimationKey(x,y),tupleList)
    return list(map(lambda x_y: nuke.AnimationKey(x_y[0], x_y[1]), tupleList))

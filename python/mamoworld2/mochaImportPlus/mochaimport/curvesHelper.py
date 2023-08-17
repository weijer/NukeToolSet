import nuke


def getLayersAsList(curves):
    return getLayersAsListHelper(curves.rootLayer, [curves.rootLayer])


def getLayersAsListHelper(layer, _list):
    for i in layer:
        x = i.getAttributes()
        if isinstance(i, nuke.rotopaint.Shape):
            _list.append(i)
        if isinstance(i, nuke.rotopaint.Stroke):
            _list.append(i)
        if isinstance(i, nuke.rotopaint.Layer):
            _list.append(i)
            getLayersAsListHelper(i, _list)
    return _list


def layerListToLayerNameList(layerList):
    return list(map(lambda x: x.name, layerList))

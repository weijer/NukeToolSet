import nuke, nukescripts, nuke.rotopaint as rp, nuke.splinewarp as sw, math
import time, threading
import sys, os, uuid
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    '''
    function to make the generated xml more human read friendly
    '''
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def rptsw_walker(obj, list):
    '''
    Returns the Rotopaint node tree [item, parentofitem, uuid]
    '''
    for i in obj:
        if isinstance(i, nuke.rotopaint.Shape):
            # uuid to take care of repeated names
            list.append([i, obj, str(uuid.uuid4())])
        if isinstance(i, nuke.rotopaint.Layer):
            list.append([i, obj, str(uuid.uuid4())])
            rptsw_walker(i, list)
    return list


def rptsw_TransformToMatrix(point, transf, f):
    '''
    Returns the vector position of a 2d point passing through a transform matrix 
    '''
    extramatrix = transf.evaluate(f).getMatrix()
    vector = nuke.math.Vector4(point[0], point[1], 1, 1)
    x = (vector[0] * extramatrix[0]) + (vector[1] * extramatrix[1]) + extramatrix[2] + extramatrix[3]
    y = (vector[0] * extramatrix[4]) + (vector[1] * extramatrix[5]) + extramatrix[6] + extramatrix[7]
    z = (vector[0] * extramatrix[8]) + (vector[1] * extramatrix[9]) + extramatrix[10] + extramatrix[11]
    w = (vector[0] * extramatrix[12]) + (vector[1] * extramatrix[13]) + extramatrix[14] + extramatrix[15]
    vector = nuke.math.Vector4(x, y, z, w)
    vector = vector / w
    return vector


def rptsw_TransformLayers(point, Layer, f, rotoRoot, rptsw_shapeList):
    '''
    Returns the vector position of a 2d point passing through a series
    of Layers transform matrices until reaching the Root Layer     
    '''

    if Layer == rotoRoot:
        transf = Layer.getTransform()
        newpoint = rptsw_TransformToMatrix(point, transf, f)

    else:
        transf = Layer.getTransform()
        newpoint = rptsw_TransformToMatrix(point, transf, f)
        for x in rptsw_shapeList:  # look the layer parent
            if x[0] == Layer:
                newpoint = rptsw_TransformLayers(newpoint, x[1], f, rotoRoot, rptsw_shapeList)
    return newpoint


def worldToImageTransform(value, rotoNode, axis):
    """
    Converts values to Silhouette values (Image transform, project resolution independent)
    """
    nodeFormat = rotoNode['format'].value()
    if axis == "x":
        transform = ((value - (nodeFormat.width() / 2)) / nodeFormat.height()) * nodeFormat.pixelAspect()
    else:
        transform = ((nodeFormat.height() - value) - (nodeFormat.height() / 2)) / nodeFormat.height()
    return transform


def parseShapeFlags(flags):
    flaglist = []
    NukeFlags = ["eBreakFlag", "eTangentLengthLockFlag", "eKeySelectedFlag",
                 "eLeftTangentSelectedFlag", "eRightTangentSelectedFlag",
                 "eOpenFlag", "eSelectedFlag", "eActiveFlag", "eVisibleFlag",
                 "eRenderableFlag", "eLockedFlag", "ePressureInZFlag", "eNukeAnimCurveEvalFlag",
                 "eRelativeTangentFlag"]
    # allflags = "000000000011111111111111"
    # ===========================================================================
    # converts integers to binary for flag check
    # ===========================================================================
    getBin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)
    binflags = getBin(flags, len(NukeFlags))
    for pos in range(0, len(NukeFlags)):
        if binflags[pos] == "1":
            flaglist.append(NukeFlags[len(NukeFlags) - 1 - pos])
    return flaglist


def createLayers(layer, fRange, rotoNode, rptsw_shapeList, task2, fxsExport, bakeshapes):
    '''
    Creates the layer xml and assigns it to the fxsExport parent
    #===========================================================================
    # <Layer type="Layer" id="0" label="Layer 1" selected="True" expanded="True" uuid="6BFA7E72-AB79-48A7-BC5A-079A8F5651C8">
    #===========================================================================
    '''
    global cancel
    rotoCurve = rotoNode['curves']
    rotoRoot = rotoCurve.rootLayer
    transf = layer[0].getTransform()
    allAttributes = layer[0].getAttributes()
    # =*=*=*=*=*=*===========================================================
    task = nuke.ProgressTask('Layer Exporter')
    task.setMessage('Creating Layer: %s' % layer[0].name)
    # =*=*=*=*=*=*===========================================================
    if layer[0].name == layer[1].name:  # (its the root)
        fxsLayer = ET.SubElement(fxsExport, 'Layer', {'type': 'Layer', 'label': layer[0].name, 'expanded': 'True'})
    else:
        layermatch = False
        layerlist = fxsExport.findall('.//Object')
        for layeritem in layerlist:
            if layeritem.get('label') == layer[1].name:
                layermatch = True
                obj = layeritem.findall("Properties/Property")
                for item in obj:
                    if item.get('id') == "objects":
                        fxsLayer = ET.SubElement(item, 'Object',
                                                 {'type': 'Layer', 'label': layer[0].name, 'expanded': 'True'})
                break
        if not layermatch:
            layerlist = fxsExport.findall('.//Layer')
            for layeritem in layerlist:
                if layeritem.get('label') == layer[1].name:
                    layermatch = True
                    obj = layeritem.findall("Properties/Property")
                    for item in obj:
                        if item.get('id') == "objects":
                            fxsLayer = ET.SubElement(item, 'Object',
                                                     {'type': 'Layer', 'label': layer[0].name, 'expanded': 'True'})
                    break

    fxsProperties = ET.SubElement(fxsLayer, 'Properties')
    # ===========================================================================
    # Layer color - Silhouette default color
    # ===========================================================================
    fxsColor = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'color'})
    fxsColorValue = ET.SubElement(fxsColor, 'Value')
    fxsColorValue.text = "(1.000000,1.000000,1.000000)"
    # ===========================================================================
    # shape overlay color end
    # ===========================================================================
    fxsInvert = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'invert'})
    fxsInvertValue = ET.SubElement(fxsInvert, 'Value')
    fxsInvertValue.text = "false"
    fxsMode = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'mode'})
    fxsModeValue = ET.SubElement(fxsMode, 'Value')
    fxsModeValue.text = "Add"
    # ===========================================================================
    # adds matrix data to the layer
    # ===========================================================================
    if not bakeshapes:
        matrixtoLayer(layer, fRange, rotoNode, rptsw_shapeList, task, fxsProperties)
    # ===========================================================================
    # ADD empty object tag for the child shapes
    # ===========================================================================
    fxsObj = ET.SubElement(fxsProperties, 'Property', {'id': 'objects', 'constant': 'True', 'expanded': 'True'})
    # =*=*=*=*=*=*==task=related=code========================================
    taskLenght = len(layer[0])
    taskCount = 0
    # =*=*=*=*=*=*==task=related=code========================================
    for item in rptsw_shapeList[::-1]:  # create all shapes in this layer
        if isinstance(item[0], nuke.rotopaint.Shape) and item[1].name == layer[0].name:
            # =*=*=*=*=*=*==task=related=code========================================
            taskCount += 1
            task.setProgress(int(taskCount / taskLenght * 100))
            if task.isCancelled():
                cancel = True
                break
            if cancel:
                break
            # =*=*=*=*=*=*==task=related=code========================================
            createShapes(item, fRange, rotoNode, rptsw_shapeList, task2, fxsExport, bakeshapes)


def createShapes(shape, fRange, rotoNode, rptsw_shapeList, task2, fxsExport, bakeshapes):
    # =*=*=*=*=*=*==task=related=code========================================
    task = nuke.ProgressTask('Shape Exporter')
    task.setMessage('Creating Shape: %s' % shape[0].name)
    # =*=*=*=*=*=*===========================================================
    # ===========================================================================
    # CHECK FOR 1 POINT SHAPE AND IGNORE IT, Silhouette doesn't like this
    # ===========================================================================
    if len(shape[0]) <= 1:
        return
    curvetype = ""
    shapeRawInfo = shape[0].serialise()
    shapeRawInfo = shapeRawInfo.split('\n')
    if [True for string in ["{curvegroup ", "{cubiccurve "] if shapeRawInfo[0].count(string) > 0]:
        curve = shapeRawInfo[0].split()
        curvetype = curve[3]
    shapetype = "Bezier" if curvetype == "bezier" else "Bspline"
    # ===========================================================================
    # get shape flags / cubic curve flags
    # ===========================================================================
    try:
        # =======================================================================
        # not sure what happens here, perhaps a bug on Nuke Roto serialization
        # sometimes if layers or shapes are selected on the UI the serialization fails
        # added the error handling below to warn users
        # =======================================================================
        shapeFlags = int(shapeRawInfo[0].split()[2])
    except:
        if nuke.GUI:
            nuke.delete(rotoNode)  # clean up cloned node
            nuke.message('ERROR! Aborting Script.\nDeselect any curves/layers on the node before running it again.')

    shapeFlags = parseShapeFlags(shapeFlags)
    ccshapeFlags = shapeRawInfo[2]
    ccshapeFlags = int(ccshapeFlags[1:-1].split()[1])
    ccshapeFlags = parseShapeFlags(ccshapeFlags)
    # ===========================================================================
    global cancel
    rotoCurve = rotoNode['curves']
    rotoRoot = rotoCurve.rootLayer
    transf = shape[0].getTransform()
    allAttributes = shape[0].getAttributes()
    # ===========================================================================
    # visibility
    # ===========================================================================
    hidden = "True" if allAttributes.getValue(0, 'vis') == 0 else "False"
    locked = "True" if "eLockedFlag" in shapeFlags else "False"
    # ===========================================================================
    # visibility end
    # ===========================================================================
    # ===========================================================================
    # Assign shapes to parent layers
    # ===========================================================================
    layerlist = fxsExport.findall('Layer')
    layermatch = False
    for layer in layerlist:
        if layer.get('label') == shape[1].name:
            layermatch = True
            obj = layer.findall("Properties/Property")
            for item in obj:
                if item.get('id') == "objects":
                    fxsShape = ET.SubElement(item, 'Object',
                                             {'type': 'Shape', 'label': shape[0].name, 'shape_type': shapetype,
                                              'hidden': hidden, 'locked': locked})
            break
    if not layermatch:
        layerlist = fxsExport.findall('.//Object')
        for layer in layerlist:
            if layer.get('label') == shape[1].name:
                obj = layer.findall("Properties/Property")
                for item in obj:
                    if item.get('id') == "objects":
                        fxsShape = ET.SubElement(item, 'Object',
                                                 {'type': 'Shape', 'label': shape[0].name, 'shape_type': shapetype,
                                                  'hidden': hidden, 'locked': locked})
                break

    fxsProperties = ET.SubElement(fxsShape, 'Properties')
    # ===========================================================================
    # opacity export
    # ===========================================================================
    for n in range(0, len(allAttributes)):
        if allAttributes.getName(n) == "opc":
            opcindex = n
            break
    if allAttributes.getCurve('opc').getNumberOfKeys() > 0:
        fxsOpacity = ET.SubElement(fxsProperties, 'Property', {'id': 'opacity'})
        for key in range(0, allAttributes.getCurve('opc').getNumberOfKeys()):
            # ===================================================================
            # interpolation 257 = HOLD            
            # ===================================================================
            keyinterpolation = allAttributes.getCurve('opc').getKey(key).interpolationType
            keyinterpolation = "hold" if keyinterpolation == 257 else "linear"

            fxsOpcKey = ET.SubElement(fxsOpacity, 'Key',
                                      {'frame': str(allAttributes.getKeyTime(opcindex, key) - nuke.root().firstFrame()),
                                       'interp': keyinterpolation})
            fxsOpcKey.text = str(allAttributes.getValue(allAttributes.getKeyTime(opcindex, key), 'opc') * 100)
    else:
        fxsOpacity = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'opacity'})
        fxsOpacityValue = ET.SubElement(fxsOpacity, 'Value')
        fxsOpacityValue.text = str(allAttributes.getValue(allAttributes.getKeyTime(opcindex, 0), 'opc') * 100)
    # ===========================================================================
    # end of opacity        
    # ===========================================================================
    # ===========================================================================
    # shape motion blur start
    # ===========================================================================
    fxsMblur = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'motionBlur'})
    fxsMblurValue = ET.SubElement(fxsMblur, 'Value')
    fxsMblurValue.text = "false" if allAttributes.getValue(0, 'mbo') == 0 else "true"
    # ===========================================================================
    # shape motion blur end
    # ===========================================================================
    # ===========================================================================
    # shape overlay color
    # ===========================================================================
    fxsOutlineColor = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'outlineColor'})
    fxsOutlineColorValue = ET.SubElement(fxsOutlineColor, 'Value')

    r = allAttributes.getValue(0, 'ro')
    g = allAttributes.getValue(0, 'go')
    b = allAttributes.getValue(0, 'bo')
    if r == 0.0 and g == 0.0 and b == 0.0:  # if default Nuke "black/none" color, change it to red
        fxsOutlineColorValue.text = "(1.0,0.0,0.0)"
    else:
        fxsOutlineColorValue.text = "(" + str(r) + "," + str(g) + "," + str(b) + ")"
    # ===========================================================================
    # shape overlay color end
    # ===========================================================================
    # ===========================================================================
    # shape blending mode
    # ===========================================================================
    fxsBlendingMode = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'mode'})
    fxsBlendingModeValue = ET.SubElement(fxsBlendingMode, 'Value')
    modes = {0: "Add", 12: "Subtract", 13: "Difference", 4: "Max", 5: "Inside"}
    if modes.get(allAttributes.getValue(0, 'bm')) != None:
        fxsBlendingModeValue.text = modes.get(allAttributes.getValue(0, 'bm'))
    else:
        fxsBlendingModeValue.text = "Add"
    # ===========================================================================
    # shape blending mode end
    # ===========================================================================
    # ===========================================================================
    # shape inverted
    # ===========================================================================
    fxsInvert = ET.SubElement(fxsProperties, 'Property', {'constant': 'True', 'id': 'invert'})
    fxsInvertedValue = ET.SubElement(fxsInvert, 'Value')
    if allAttributes.getValue(0, 'inv') == 1:
        fxsInvertedValue.text = "true"
    else:
        fxsInvertedValue.text = "false"
    # ===========================================================================
    # shape inverted end
    # ===========================================================================
    fxsPath = ET.SubElement(fxsProperties, 'Property', {'id': 'path'})
    pathclosed = False if "eOpenFlag" in ccshapeFlags else True

    # ===========================================================================
    # check if all the point elements (center and tangents) share linear/hold keyframes and store them for further optimization
    # ===========================================================================
    n = 0
    keyframeTimes = {}
    for point in shape[0]:
        pts = [point.center.getPositionAnimCurve(0), point.center.getPositionAnimCurve(1),
               point.leftTangent.getPositionAnimCurve(0), point.leftTangent.getPositionAnimCurve(1),
               point.rightTangent.getPositionAnimCurve(0), point.rightTangent.getPositionAnimCurve(1)]
        curvenames = ["cx", "cy", "ltx", "lty", "rtx", "rty"]
        for ptype in range(len(pts)):
            keys = pts[ptype].getNumberOfKeys()
            for key in range(keys):
                # ===============================================================
                # check if current key is in the dict and abort if is already invalid.
                # ===============================================================
                if pts[ptype].getKey(key).time not in keyframeTimes:
                    keyframeTimes[pts[ptype].getKey(key).time] = True
                else:
                    if keyframeTimes.get(pts[ptype].getKey(key).time):
                        acceptKeyframe = False
                        if key > 0:
                            if pts[ptype].getKey(key - 1).rslope == pts[ptype].getKey(key).lslope:
                                acceptKeyframe = True
                            if pts[ptype].getKey(key).interpolationType in ["257", "258"]:
                                acceptKeyframe = True
                        elif key == 0:
                            if pts[ptype].getKey(key).rslope == pts[ptype].getKey(key + 1).lslope and pts[ptype].getKey(
                                    key).interpolationType in [256, 257, 258]:
                                acceptKeyframe = True
                            elif keys == 1:
                                acceptKeyframe = True
                        if not acceptKeyframe:
                            keyframeTimes[pts[ptype].getKey(key).time] = False
        n += 1

    keys = sorted(keyframeTimes.items(), key=lambda x: x[0])
    # ===========================================================================
    # removes unwanted keyframes before fRange start, avoiding errors on the subsequent code
    # ===========================================================================
    for key in range(len(keys))[::-1]:
        if keys[key][0] < int(fRange.first()):
            keys.pop(key)

    if len(keys) == 0:  # safeguard for shapes that have no keyframes at all
        keys.append([fRange.first(), True])

    # ===========================================================================
    # Creates the keyframes for the curve points
    # skipping baked frames for linear/hold keyframes that silhouette can handle
    # all the other interpolation types are baked
    # ===========================================================================
    n = 0
    for f in fRange:
        if not keys[n][1] and f <= keys[n][0] or keys[n][1] and f == keys[n][0] or f in [fRange.first(), fRange.last()]:

            fxsPathKey = ET.SubElement(fxsPath, 'Key', {'frame': str(f - nuke.root().firstFrame()), 'interp': 'linear'})
            fxsPathKeyPath = ET.SubElement(fxsPathKey, 'Path', {'closed': str(pathclosed), 'type': shapetype})
            taskCount = 0
            for point in shape[0]:
                # =*=*=*=*=*=*==task=related=code========================================
                task.setMessage(
                    'Working ' + shape[0].name + ' point ' + str(taskCount + 1) + " of " + str(len(shape[0])))
                taskCount += 1
                task.setProgress(int(taskCount / len(shape[0]) * 100))
                if task.isCancelled():
                    cancel = True
                    break
                if cancel:
                    break
                # =*=*=*=*=*=*==task=related=code========================================
                point_c = [point.center.getPositionAnimCurve(0).evaluate(f),
                           point.center.getPositionAnimCurve(1).evaluate(f)]
                point_lt = [point.center.getPositionAnimCurve(0).evaluate(f) + (
                point.leftTangent.getPositionAnimCurve(0).evaluate(f) * -1),
                            point.center.getPositionAnimCurve(1).evaluate(f) + (
                            point.leftTangent.getPositionAnimCurve(1).evaluate(f) * -1)]
                point_rt = [point.center.getPositionAnimCurve(0).evaluate(f) + (
                point.rightTangent.getPositionAnimCurve(0).evaluate(f) * -1),
                            point.center.getPositionAnimCurve(1).evaluate(f) + (
                            point.rightTangent.getPositionAnimCurve(1).evaluate(f) * -1)]
                transf = shape[0].getTransform()
                if bakeshapes:  # bake the point position based on shape/parent layers transforms
                    point_c = rptsw_TransformToMatrix(point_c, transf, f)
                    point_c = rptsw_TransformLayers(point_c, shape[1], f, rotoRoot, rptsw_shapeList)
                    point_lt = rptsw_TransformToMatrix(point_lt, transf, f)
                    point_lt = rptsw_TransformLayers(point_lt, shape[1], f, rotoRoot, rptsw_shapeList)
                    point_rt = rptsw_TransformToMatrix(point_rt, transf, f)
                    point_rt = rptsw_TransformLayers(point_rt, shape[1], f, rotoRoot, rptsw_shapeList)

                x = point_c[0]
                y = point_c[1]
                ltx = point_lt[0]
                rtx = point_rt[0]
                lty = point_lt[1]
                rty = point_rt[1]
                x = worldToImageTransform(x, rotoNode, "x")
                y = worldToImageTransform(y, rotoNode, "y")
                ltx = worldToImageTransform(ltx, rotoNode, "x")
                lty = worldToImageTransform(lty, rotoNode, "y")
                rtx = worldToImageTransform(rtx, rotoNode, "x")
                rty = worldToImageTransform(rty, rotoNode, "y")
                fxsPoint = ET.SubElement(fxsPathKeyPath, 'Point')  # "",text = "tst")
                if shapetype == "Bspline":
                    fxsPoint.text = "(%f,%f)" % (x, y)  # %f otherwise silhouette may reject the imported shapes.
                else:
                    fxsPoint.text = "(%f,%f),(%f,%f),(%f,%f)" % (x, y, rtx, rty, ltx, lty)
        if f == keys[n][0] and keys[n][0] != keys[-1][0]:
            n += 1
    # ===========================================================================
    # remove repeated keyframes optimization
    # ===========================================================================
    if cancel:
        return
    # =*=*=*=*=*=*==task=related=code========================================
    shapePath = fxsShape.findall(".//Path")
    removelist = []
    for n in range(len(shapePath)):  # [::-1]:
        if n > 0 and n < len(shapePath) - 1:
            totalp = 0
            for nn in range(len(shapePath[n])):
                # ===============================================================
                # remove float decimal places from the numbers for comparison
                # ===============================================================
                roundness = -3
                actual = shapePath[n][nn].text[1:-1].split(",")
                actual[0] = actual[0][:roundness]
                actual[1] = actual[1][:roundness]
                prev = shapePath[n - 1][nn].text[1:-1].split(",")
                prev[0] = prev[0][:roundness]
                prev[1] = prev[1][:roundness]
                next = shapePath[n + 1][nn].text[1:-1].split(",")
                next[0] = next[0][:roundness]
                next[1] = next[1][:roundness]
                # ===============================================================
                # Silhouette stores all the points on the same keyframe
                # so we can only delete repeated keyframes if all the points match data
                # ===============================================================
                # if this keyframe is equal to previous and next one
                if actual == prev and actual == next:
                    totalp += 1
            if totalp == len(shapePath[n]):
                removelist.append(n)
    mainpath = fxsShape.findall(".//Property")
    for prop in mainpath:
        if prop.attrib.get('id') == "path":
            keys = prop.findall(".//Key")
            keysn = len(keys) - 1
            for k in keys[::-1]:
                if keysn in removelist:
                    prop.remove(k)
                keysn -= 1


def matrixtoLayer(item, fRange, rotoNode, rptsw_shapeList, task, fxsLayer):
    '''
    Adds a transform Matrix to the Layer
    '''
    projectionMatrixTo = nuke.math.Matrix4()
    projectionMatrixFrom = nuke.math.Matrix4()
    nodeFormat = rotoNode['format'].value()
    rotoCurve = rotoNode['curves']
    rotoRoot = rotoCurve.rootLayer
    transf = item[0].getTransform()
    thematrix = ET.SubElement(fxsLayer, 'Property', {'id': 'transform.matrix'})
    for f in fRange:
        # ===========================================================================
        # node format rectangle transformed through the matrix
        # ===========================================================================
        to1 = [0.0, 0.0]
        to2 = [float(nodeFormat.width()), 0.0]
        to3 = [float(nodeFormat.width()), float(nodeFormat.height())]
        to4 = [0, float(nodeFormat.height())]
        to1 = rptsw_TransformToMatrix(to1, transf, f)
        to2 = rptsw_TransformToMatrix(to2, transf, f)
        to3 = rptsw_TransformToMatrix(to3, transf, f)
        to4 = rptsw_TransformToMatrix(to4, transf, f)
        # ===========================================================================
        # convert it to Silhouette ImageTransform coordinates
        # ===========================================================================
        to1x = worldToImageTransform(to1[0], rotoNode, "x")
        to2x = worldToImageTransform(to2[0], rotoNode, "x")
        to3x = worldToImageTransform(to3[0], rotoNode, "x")
        to4x = worldToImageTransform(to4[0], rotoNode, "x")
        to1y = worldToImageTransform(to1[1], rotoNode, "y")
        to2y = worldToImageTransform(to2[1], rotoNode, "y")
        to3y = worldToImageTransform(to3[1], rotoNode, "y")
        to4y = worldToImageTransform(to4[1], rotoNode, "y")
        # ===========================================================================
        # from = Silhouette image coordinate system: -0.5 on top y, 0.5 on bottom y, x is dependent on the format size
        # ===========================================================================
        from1x = worldToImageTransform(0.0, rotoNode, "x")
        from1y = 0.5
        from2x, from2y = [worldToImageTransform(float(nodeFormat.width()), rotoNode, "x"), 0.5]
        from3x, from3y = [worldToImageTransform(float(nodeFormat.width()), rotoNode, "x"), -0.5]
        from4x, from4y = [worldToImageTransform(0.0, rotoNode, "x"), -0.5]

        projectionMatrixTo.mapUnitSquareToQuad(to1x, to1y, to2x, to2y, to3x, to3y, to4x, to4y)
        projectionMatrixFrom.mapUnitSquareToQuad(from1x, from1y, from2x, from2y, from3x, from3y, from4x, from4y)
        theCornerpinAsMatrix = projectionMatrixTo * projectionMatrixFrom.inverse()
        matrixkey = ET.SubElement(thematrix, 'Key', {'frame': str(f - nuke.root().firstFrame()),
                                                     'interp': 'linear'})  # it was fRange.first()
        # =======================================================================
        # format the matrix keyframe data string
        # =======================================================================
        matrixline = ""
        for n in range(len(theCornerpinAsMatrix)):
            matrixline += "%f" % theCornerpinAsMatrix[n]
            if n < 15:
                matrixline += ","
        matrixkey.text = "(" + matrixline + ")"

        # ===========================================================================
        # remove repeated keyframes optimization
        # ===========================================================================
        # =*=*=*=*=*=*==task=related=code========================================
        if cancel:
            return
        # =*=*=*=*=*=*==task=related=code========================================
        layerProps = fxsLayer.findall(".//Property")
        removelist = []
        for prop in layerProps:
            if prop.attrib.get('id') == "transform.matrix":
                keys = prop.findall(".//Key")
                for n in range(len(keys)):  # [::-1]:
                    if n > 0 and n < len(keys) - 1:
                        if keys[n].text == keys[n - 1].text and keys[n].text == keys[n + 1].text:
                            removelist.append(n)
        mainpath = fxsLayer.findall(".//Property")
        for prop in mainpath:
            if prop.attrib.get('id') == "transform.matrix":
                keys = prop.findall(".//Key")
                keysn = len(keys) - 1
                for k in keys[::-1]:
                    if keysn in removelist:
                        prop.remove(k)
                    keysn -= 1


def checkEqualTransform(shape1, shape2, fRange):
    '''
    Compares 2 shapes transform data
    Used to identify identical transforms and group shapes inside the same tracked layer
    '''
    check = True
    shape1Transf = shape1.getTransform()
    shape2Transf = shape2.getTransform()
    for f in fRange:
        m1 = shape1Transf.evaluate(f).getMatrix()
        m2 = shape2Transf.evaluate(f).getMatrix()
        if m1 != m2:
            check = False
            break
    return check


def manageTransforms(fRange, rotoNode, rptsw_shapeList):  # ,task):
    '''
    Creates new parent Layers and transfer shapes transforms to them
    '''
    global cancel
    rotoCurve = rotoNode['curves']
    createdShapes = []
    # =*=*=*=*=*=*==task=related=code========================================
    task = nuke.ProgressTask('Manage Transforms')
    taskCount = 0
    taskLenght = len(rptsw_shapeList)
    # =*=*=*=*=*=*==task=related=code========================================
    for item in rptsw_shapeList:
        # =*=*=*=*=*=*==task=related=code========================================
        task.setMessage('Preparing Shapes and Layers')
        if cancel:
            return
        task.setProgress(int(taskCount / taskLenght * 100))
        taskCount += 1
        # =*=*=*=*=*=*==task=related=code========================================
        if isinstance(item[0], nuke.rotopaint.Shape):
            # ===================================================================
            # optimization: verify if shapes share the very same transform data and put them on the same layer
            # ===================================================================
            sametransform = False
            for shape in createdShapes:
                if shape[1].name == item[1].name:  # share the same parent
                    if checkEqualTransform(item[0], shape[0], fRange):
                        sametransform = True
                        sameparent = shape[3]
                        break
            createdShapes.append(item)
            # ===================================================================
            shapeTransf = item[0].getTransform()
            if len(item[1]) > 1:  # apply to a new layer
                if not sametransform:
                    newLayer = rp.Layer(rotoCurve)
                    newLayer.name = item[0].name + "_trkdata"
                    newLayer.setTransform(shapeTransf)
                    item[1].append(newLayer)
                    newLayer.append(item[0])
                    createdShapes[-1].append(newLayer)
                else:
                    sameparent.append(item[0])
            else:
                # ===============================================================
                # this shape is single child, transfer the transform data to the parent layer
                # ===============================================================
                newLayer = rp.Layer(rotoCurve)  # temp Layer to hold the data
                newLayerTransf = newLayer.getTransform()
                matrixCurves = []
                for i in range(4):
                    matrixCurves.append([])
                    for j in range(4):
                        matrixCurves[i].append(newLayerTransf.getExtraMatrixAnimCurve(i, j))
                parentTranf = item[1].getTransform()
                for f in fRange:
                    m1 = shapeTransf.evaluate(f).getMatrix()
                    m2 = parentTranf.evaluate(f).getMatrix()
                    m3 = m2 * m1
                    m = 0
                    for i in range(4):
                        for j in range(4):
                            matrixCurves[i][j].addKey(f, m3.__getitem__(m))
                            m += 1
                newLayerTransf = newLayer.getTransform()
                item[1].setTransform(newLayerTransf)


def uniqueNames(list):
    '''
    Adds uuids to not unique Layer/Shapes names found
    Nuke doesn't allows repeated names, but other softwares like Silhouette may export repeated names to Nuke
    '''
    nameList = []
    for item in list:
        if item[0].name not in nameList:
            nameList.append(item[0].name)
        else:
            item[0].name = item[0].name + "_" + item[2]


def silhouetteFxsExporter():
    '''
    Main exporter code, UI 
    '''
    try:
        rotoNode = nuke.selectedNode()
        if rotoNode.Class() not in ('Roto', 'RotoPaint'):
            if nuke.GUI:
                nuke.message('Unsupported node type. Selected Node must be Roto or RotoPaint')
            return
    except:
        if nuke.GUI:
            nuke.message('Select a Roto or RotoPaint Node')
            return
    # ===========================================================================
    # Nuke UI panel setup
    # ===========================================================================
    p = nukescripts.panels.PythonPanel("FXS Shape Exporter")
    k = nuke.String_Knob("framerange", "FrameRange")
    k.setFlag(nuke.STARTLINE)
    k.setTooltip("Set the framerange to bake the shapes, by default its the project start-end. Example: 10-20")
    p.addKnob(k)
    k.setValue("%s-%s" % (nuke.root().firstFrame(), nuke.root().lastFrame()))
    k = nuke.Boolean_Knob("bake", "Bake Shapes")
    k.setFlag(nuke.STARTLINE)
    k.setTooltip("Export the shapes baking keyframes and transforms")
    p.addKnob(k)
    result = p.showModalDialog()

    if result == 0:
        return  # Canceled
    try:
        fRange = nuke.FrameRange(p.knobs()["framerange"].getText())
    except:
        if nuke.GUI:
            nuke.message('Framerange format is not correct, use startframe-endframe i.e.: 0-200')
        return
    # ===========================================================================
    # end of panel
    # ===========================================================================
    start_time = time.time()
    rptsw_shapeList = []
    global cancel
    cancel = False

    if nuke.NUKE_VERSION_MAJOR > 6:
        # =======================================================================
        # creates a copy of the node to modify and keep original safe
        # =======================================================================
        nukescripts.node_copypaste()
        # =======================================================================
        bakeshapes = p.knobs()["bake"].value()
        rptsw_shapeList = []
        rotoNode = nuke.selectedNode()
        rotoCurve = rotoNode['curves']
        rotoRoot = rotoCurve.rootLayer
        # =*=*=*=*=*=*==task=related=code========================================
        task = nuke.ProgressTask('FXS Shape Exporter')
        task.setMessage('Starting FXS export')
        task.setProgress(10)
        # =*=*=*=*=*=*==task=related=code========================================
        rptsw_shapeList = rptsw_walker(rotoRoot, rptsw_shapeList)
        # =======================================================================
        # creates additional layers to handle shape transforms
        # =======================================================================
        # =*=*=*=*=*=*==task=related=code========================================
        task.setMessage('Sorting out Transforms')
        task.setProgress(20)
        # =*=*=*=*=*=*==task=related=code========================================
        uniqueNames(rptsw_shapeList)
        if not bakeshapes:
            manageTransforms(fRange, rotoNode, rptsw_shapeList)  # ,task)
        # =*=*=*=*=*=*==task=related=code========================================
        if cancel:
            return
        # =*=*=*=*=*=*==task=related=code========================================
        rotoCurve.changed()  # just for debugging purposes
        # =======================================================================
        rptsw_shapeList = []
        rptsw_shapeList = rptsw_walker(rotoRoot, rptsw_shapeList)
        nodeFormat = rotoNode['format'].value()
        fxsExport = ET.Element('Silhouette', {'width': str(nodeFormat.width()), 'height': str(nodeFormat.height()),
                                              'workRangeStart': str(fRange.first()), 'workRangeEnd': str(fRange.last()),
                                              'sessionStartFrame': str(fRange.first())})
        # =======================================================================
        # create the root layer first
        # =======================================================================
        item = [rotoRoot, rotoRoot]
        createLayers(item, fRange, rotoNode, rptsw_shapeList, task, fxsExport, bakeshapes)
        # =*=*=*=*=*=*==task=related=code========================================
        task.setMessage('Creating Layers')
        task.setProgress(30)
        taskLength = len(rptsw_shapeList)
        taskCount = 0.0
        # =*=*=*=*=*=*==task=related=code========================================
        # =======================================================================
        # create all layers and shapes inside them
        # =======================================================================
        for item in rptsw_shapeList:
            taskCount += 1.0
            x = (taskCount / taskLength) * 10 + 30
            task.setProgress(30 + int((taskCount / taskLength) * 20))
            # =*=*=*=*=*=*==task=related=code========================================
            if cancel:
                break
            # =*=*=*=*=*=*==task=related=code========================================
            if isinstance(item[0], nuke.rotopaint.Layer):
                createLayers(item, fRange, rotoNode, rptsw_shapeList, task, fxsExport, bakeshapes)
        # ===================================================================
        # reorder layers/shapes
        # ===================================================================
        layerlist = []
        for item in rptsw_shapeList[::-1]:
            if item[1].name not in layerlist:  # find all parent names
                layerlist.append(item[1].name)
        # =*=*=*=*=*=*==task=related=code========================================
        task.setMessage('Reordering Layer/Shapes')
        task.setProgress(50)
        taskLength = len(rptsw_shapeList)
        taskCount = 0.0
        # =*=*=*=*=*=*==task=related=code========================================
        for name in layerlist:
            # =*=*=*=*=*=*==task=related=code========================================
            task.setProgress(50 + int((taskCount / taskLength) * 50))
            taskCount += 1.0
            if cancel:
                break
            # =*=*=*=*=*=*==task=related=code========================================
            data = []
            parentElement = []
            for item in rptsw_shapeList[::-1]:
                if item[1].name == name:  # all items from same parent
                    for itemx in fxsExport.findall('.//*'):
                        if itemx.get('label') != None:
                            if item[0].name == itemx.get('label'):
                                if itemx not in data:
                                    data.append(itemx)  # locate the elements of that parent
            for itemx in fxsExport.findall('.//*'):
                if itemx.get('label') == name:
                    obj = itemx.findall("Properties/Property")
                    for item in obj:
                        if item.get('id') == "objects":
                            parentElement.append(item)
                            break
            for n in range(len(data)):
                parentElement[0][n] = data[n]
                # ===================================================================
                # end of reorder layers/shapes
                # ===================================================================
    else:
        nuke.message('Shape Exporter is for Nuke v7 only')

    # =*=*=*=*=*=*==task=related=code========================================
    if cancel:
        nuke.delete(rotoNode)
        return
    # =*=*=*=*=*=*==task=related=code========================================

    # ===========================================================================
    # EXPORT the fxs file
    # ===========================================================================
    path = os.getenv('FXSEXPORTPATH')
    if path == None:
        path = nuke.getFilename('Save the .fxs file', '*.fxs', "fxsExport.fxs")
        if path == None:
            if nuke.GUI:
                nuke.message('Aborting Script, you need to save the export to a file')
                return
        else:
            base = os.path.split(path)[0]
            ext = os.path.split(path)[1][-4:]
            # ==================================================================
            # adds extension if not present on the filename
            # ==================================================================
            if ext != ".fxs":
                ext = ext + ".fxs"
                path = os.path.join(base, ext)
    else:
        print "Saving file to: %s" % path

    indent(fxsExport)
    ET.ElementTree(fxsExport).write(path)
    nuke.delete(rotoNode)
    task.setProgress(100)
    print "Time elapsed: %s seconds" % (time.time() - start_time)


if __name__ == '__main__':
    silhouetteFxsExporter()

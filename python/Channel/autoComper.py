#######################################################################################################
#  autoComper V1.2 - Date: 17.09.2011 - Created by Jan Oberhauser - jan.oberhauser@gmail.com          #
#  Creates a ready to start script on the push of a button                                            #
#  Check for a updateted Version at http://janoberhauser.gute-filme-enden-nie.de                      #
#######################################################################################################

# How to Comp the different Channels
# -------------------------------------
# EXPLANATION:
# Here you can define the Channels/Layers/Files (from now on just Channel) to look for and their order. You dont have enter the full name of the channel if its
# called "Thatever_Diffuse_WhatDoIKnow" it is enough to just put "diffuse" (always Lower-Case) in the Channel then its gonna find it. The Scripts find them if they
# are part of the Channel-Name or if it just has one Channel it look also for the File-Name. If you have more then one Channel with the same Name-Part you can just use the
# "notCompNodes"-Variable to exclude Channels. It is always just the Channel to comp and the Parent in Lower-Case (except the START which has to be in Capitals)
# The Script has two modes. Either it just ignores the defined Comp-Channels if they are not found, or it creates a not connected Shuffle and Merge anyway
# to connect them later with other Nodes. You can switch the Modes with the Variable "createNotFoundChannels".
# and then hock-up the other Readers to the shuffels by yourself.
# DESCRIPTION: compNodes = {"FIRST_CHANNEL_NAME":"START", "SECOND_CHANNEL_NAME":"PARENT_CHANNEL", "THIRD_CHANNEL_NAME":"PARENT_CHANNEL", .., ..}
# EXAMPLE: starts with the "paint"-Channel, then "diffuse", then "specular", then "refl", then "occlusion", then depth
compNodes = {"paint": "START", "indirect_diffuse": "paint", "direct_diffuse": "indirect_diffuse",
             "indirect_specular": "direct_diffuse", "direct_specular": "indirect_specular", "refl": "direct_specular",
             "refr": "refl", "AO": "refr", "depth": "AO"}

# Now you can define which Node shall be created and connected with that found Channel and also which values it should have. So you can create any node Nuke
# offers. A Merge-Node with the Operation and the Mix-Value, a Copy-Node with the Copy-Channels, ... , .. or whatever
# You can set as many Start-Values as you want, just seperate them by a ";"
# DESCRIPTION: compNodeOperations = {"CHANNELNAME":"NODENAME:KNOBNAME=VALUE;KNOBNAME=VALUE;KNOBNAME=VALUE", "CHANNELNAME":"NODENAME:KNOBNAME=VALUE", "CHANNELNAME":"NODENAME:", .., ..}
compNodeOperations = {"direct_diffuse": "Merge:operation='plus';mix=1",
                      "indirect_diffuse": "Merge:operation='plus';mix=1",
                      "direct_specular": "Merge:operation='plus';mix=1",
                      "indirect_specular": "Merge:operation='plus';mix=1", "refl": "Merge:operation='plus';mix=1",
                      "refr": "Merge:operation='plus';mix=1", "AO": "Merge:operation='mult';mix=0.15",
                      "depth": "Copy:from0='rgba.red';to0='depth.Z'"}

# With this both variables you can create more Nodes. The Variable "addNodesBeforeComped" defines Nodes which should be created BEFORE the Channel gets
# connected with the Main-Tree. So if for example a Grade node for the depth-Channel or a ColorCorrection for the paint
# The Variable "addNodesAfterComped" defines Nodes which are created after the Channel is connected with the Main-Tree. So for Example a ZBlur-Node for the
# depth-Channel. The Syntax is the same like in the "compNodeOperations" above. I hope it is not to confusing! Probably it is the best just to select a few Nodes
# and start the Script. Then you can easily see what is created and then it is not complicated any more. And if I am wrong with that just write me a mail.
# It is also possible to create more then just one Node. All you have to do then is to sperate them with "|". Then the Nodes will get created in the same
# order you defined them. An example is the diffuse Channel bellow. It creates an Unpremult, Grade and then a Premult Node before it merges it in the Main-Tree.
addNodesBeforeComped = {"paint": "ColorCorrect:", "diffuse": "Unpremult:|Grade:|Premult:", "specular": "Grade:",
                        "refl": "Grade:", "refr": "Grade:", "AO": "Grade:", "depth": "Grade:"}
addNodesAfterComped = {"depth": "ZBlur:"}

# Which Channels should not be found
# -------------------------------------
# EXPLANATION:
# If you have for example more Channels with the same name-parts like "paint", "rotopaint", "carpaint" then you can just type in the
# channls which should not be found
# DESCRIPTION: notCompNodes = {"FIRST_LAYER":"NOT_TO_BE_FOUND_1:NOT_TO_BE_FOUND_2:NOT_TO_BE_FOUND_3", "SECOND_LAYER":"NOT_TO_BE_FOUND_1", ..., }
notCompNodes = {"paint": "rotopaint:carpaint"}

# Create Not-Found-Channels
# EXPLANATION:
# If this is set to True then it created for each Channel in compNodes a Shuffle, NoOp and Merge Node even if it is not found. This can be useful if
# this Channels come from different Files then the selected ones.
createNotFoundChannels = False

# Align the readers automatically
autoAlignReaders = True
# Create the NoOp-Node beween the Shuffle and the Merge?
createNoOpNode = True
# Create the Dot-Node beween the NoOp and the Merge?
createDotNode = True
# Show Dot-Label?
showDotLabel = True

# Color of the NoOp-Nodes after the Shuffle-Node
noOpTileColor = 0x9b00ff

# Set the Node-Positon-Offset
nodeXOffset = 180
nodeYOffset = 150

#######################################################################################################
#                                                                                                     #
#              NO CHANGES FROM HERE: (OR JUST IF YOU KNOW WHAT YOU ARE DOING)                         #
#                                                                                                     #
#######################################################################################################
import nuke


def getParentNode(layer, compNodes, mergeLayer):
    iteration = 0
    parentNode = layer
    while True:
        parentNode = compNodes[parentNode]
        if parentNode in mergeLayer:
            break

        if parentNode == 'START':
            break

        iteration += 1
        if iteration > 20:
            print "ERROR:\nPLEASE CHECK IF THE NAMES OF THE PARENT-NAMES FIT TO THE LAYER-NAMES"
            parentNode = -1
            break

    return parentNode


def calculateAdditionalYOffset(additionalYOffset, nodeToAddCount, nodeYOffset, nodeNumber):
    if nodeToAddCount * 40 > nodeYOffset:
        if nodeNumber > 1:
            if nodeNumber == 2:
                additionalYOffset = 0
            additionalYOffset += (nodeToAddCount * 40) - (nodeYOffset) - ((nodeNumber - 1) * nodeYOffset)
        else:
            additionalYOffset += (nodeToAddCount * 40) - (nodeYOffset)
    return additionalYOffset


def createNode(layer, nodeOperations, xPos, yPos):
    operationNode = nodeOperations.split(':')
    operationParameters = operationNode[1].split(';')
    operationNode = operationNode[0]

    exec ('thisNode = nuke.nodes.' + str(operationNode) + '(name="' + operationNode + ' ' + str(layer) + '")')
    thisNode.setXYpos(int(xPos), int(yPos))

    for parameter in operationParameters:
        if parameter != '':
            parameter = parameter.split('=')
            exec ("thisNode['" + parameter[0] + "'].setValue(" + parameter[1] + ")")

    return thisNode


def autoComper():
    allSelectedNodes = nuke.selectedNodes()
    mergeLayer = {}
    mergeLayerInv = {}
    layerHasReader = {}
    nodesOrdered = []
    allLayers = {}
    layerType = {}
    xPosMin = 999999
    yPosMin = 999999
    additionalYOffset = 0
    additionalYOffsetFirst = 0

    for object in compNodes:
        if compNodes[object] == 'START':
            nodesOrdered.append(object)
            break

    count = 0
    for object in compNodes:
        for object2 in compNodes:
            childNode = compNodes[object2]
            if childNode == nodesOrdered[count]:
                nodesOrdered.append(object2)
                count += 1
                break

    for thisNode in allSelectedNodes:
        thisLayers = {}
        allChannels = thisNode.channels()
        for channel in allChannels:
            thisData = str(channel.split('.')[0])
            thisLayers.update({thisData: ''})

        if len(thisLayers) == 1 and 'rgba' in thisLayers:
            fileName = thisNode['file'].getValue()
            fileName = fileName.split('/')
            fileName = fileName[len(fileName) - 1]
            fileName = fileName.split('.')[0]
            allLayers.update({fileName: thisNode})
            layerType.update({fileName: 'file'})
        else:
            for layer in thisLayers:
                allLayers.update({layer: thisNode})
                layerType.update({layer: 'channel'})

    for layer in allLayers:
        layerLower = layer.lower()

        if int(allLayers[layer]['xpos'].getValue()) < xPosMin:
            xPosMin = allLayers[layer]['xpos'].getValue()
        if int(allLayers[layer]['ypos'].getValue()) < yPosMin:
            yPosMin = allLayers[layer]['ypos'].getValue()

        for compChannel in compNodes:
            compThis = True
            if layerLower.find(compChannel, 0, len(layerLower)) > -1:
                if compChannel in notCompNodes:
                    notNodes = notCompNodes[compChannel].split(':')
                    for notNode in notNodes:
                        if layerLower.find(notNode, 0, len(layer)) > -1:
                            compThis = False
                            break

                if compThis == True:
                    mergeLayer.update({compChannel: layer})
                    mergeLayerInv.update({layer: compChannel})
                    layerHasReader.update({layer: ''})

    if createNotFoundChannels == True:
        for node in nodesOrdered:
            if node not in allLayers:
                if node not in mergeLayer:
                    mergeLayer.update({node: node})
                    mergeLayerInv.update({node: node})
    newAllLayers = []
    for node in nodesOrdered:
        if node in mergeLayer:
            newAllLayers.append(mergeLayer[node])
    for layer in allLayers:
        if layer not in newAllLayers:
            newAllLayers.append(layer)

    mergeCount = -1
    nodeNumber = -1

    for layer in newAllLayers:
        layerLower = layer.lower()
        nodeNumber += 1
        layerOriginal = layer
        if layer in mergeLayerInv:
            layer = mergeLayerInv[layer]

        if len(allSelectedNodes) > 1 and autoAlignReaders == True:
            if layerOriginal in allLayers:
                allLayers[layerOriginal].setXYpos(int(nodeNumber * nodeXOffset + xPosMin), int(yPosMin))

        if layerOriginal in layerType:
            if layerType[layerOriginal] == 'channel':
                exec (
                str(layer) + ' = nuke.nodes.Shuffle(name = "' + str(layerOriginal) + '_Shuffel", postage_stamp = True)')
                eval(layer).setXYpos(int(nodeNumber * nodeXOffset + xPosMin), int(yPosMin + 2 * nodeYOffset))
                if layerOriginal in allLayers:
                    eval(layer).setInput(0, allLayers[layerOriginal])
                    eval(layer)['in'].setValue(layerOriginal)

        if createNoOpNode:
            noOpNode = nuke.nodes.NoOp(name=layerOriginal, tile_color=noOpTileColor)
            noOpNode.setXYpos(int(nodeNumber * nodeXOffset + xPosMin), int(yPosMin + 3 * nodeYOffset))
            if layerOriginal in layerType:
                if layerType[layerOriginal] == 'file':
                    noOpNode.setInput(0, allLayers[layerOriginal])
                else:
                    noOpNode.setInput(0, eval(layer))
        else:
            if layerOriginal in layerType:
                if layerType[layerOriginal] == 'file':
                    noOpNode = allLayers[layerOriginal]
                else:
                    noOpNode = eval(layer)

        exec (layer + "noOpNode = noOpNode")

        if layer in addNodesBeforeComped:
            nodeToAddCount = 0
            nodeBefore = eval(str(layer) + "noOpNode")

            for nodeToAdd in addNodesBeforeComped[layer].split('|'):
                xPos = nodeNumber * nodeXOffset + xPosMin
                yPos = yPosMin + 4 * nodeYOffset + (nodeToAddCount * 40)
                noOpNode = createNode(layer, nodeToAdd, xPos, yPos)
                noOpNode.setInput(0, nodeBefore)

                nodeToAddCount += 1
                nodeBefore = noOpNode

            additionalYOffset = calculateAdditionalYOffset(additionalYOffset, nodeToAddCount, nodeYOffset, nodeNumber)

        if layer in mergeLayer:
            exec (layer + " = noOpNode")
            exec (layer + "Node = noOpNode")

            mergeCount += 1

            parentNode = getParentNode(layer, compNodes, mergeLayer)

            if parentNode != 'START':
                xPos = xPosMin
                yPos = mergeCount * nodeYOffset + yPosMin + 4 * nodeYOffset + additionalYOffset + additionalYOffsetFirst
                thisNode = createNode(layer, compNodeOperations[layer], xPos, yPos)

                exec (layer + "Node = thisNode")

                if mergeCount > 0 and createDotNode == True:
                    # Create Dot-Nodes
                    dot = nuke.nodes.Dot(note_font_size=20)
                    if showDotLabel:
                        dot['label'].setValue(' ' + str(layerOriginal))
                    dot.setXYpos(int(eval(layer)['xpos'].getValue() + 35), int(thisNode['ypos'].getValue() + 3))
                    dot.setInput(0, eval(layer))
                    exec (layer + " = dot")

                if layer in addNodesAfterComped:
                    nodeToAddCount = 1
                    nodeBefore = eval(str(layer) + "Node")

                    for nodeToAdd in addNodesAfterComped[layer].split('|'):
                        xPos = xPosMin
                        yPos = mergeCount * nodeYOffset + yPosMin + 4 * nodeYOffset + additionalYOffset + additionalYOffsetFirst + (
                        nodeToAddCount * 40)
                        thisNode = createNode(layer, nodeToAdd, xPos, yPos)
                        thisNode.setInput(0, nodeBefore)

                        nodeToAddCount += 1
                        nodeBefore = thisNode

                    additionalYOffsetFirst = calculateAdditionalYOffset(additionalYOffsetFirst, nodeToAddCount,
                                                                        nodeYOffset, 1)

                    exec (layer + "NodeAdd = thisNode")

    for layer in mergeLayer:
        parentNode = getParentNode(layer, compNodes, mergeLayer)

        if parentNode != 'START':
            if parentNode in addNodesAfterComped:
                parentNode = parentNode + "NodeAdd"
            else:
                parentNode = parentNode + "Node"

            exec (layer + "Node.setInput(1, " + layer + ")")
            exec (layer + "Node.setInput(0, " + str(parentNode) + ")")

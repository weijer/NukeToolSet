import nuke
import cornerPinData
import cornerPinKnobs


# This code has been used to add to the corner pin group node a callback to react to changes of the cornerpinfile knob
# extend this to also react to changes of other knobs
# (make sure the group node is selected and execute it in script editor)
#
# code = """
# import cornerPinNode
# if nuke.thisKnob().name() == 'cornerpinfile':
#    cornerPinNode.reloadTrackingData();
# """
#
# nuke.selectedNode()['knobChanged'].setValue( code ) 

# def reloadTrackingData():
#    cornerPinNode = nuke.thisNode()
#    filename = cornerPinNode['cornerpinfile'].getValue()
#    
#    try:
#        cpData = cornerPinData.CornerPinDataFromNukeCornerPinFile(filename);
#        cornerPinKnobs.applyCornerPinDataToALlKnobs(cpData,cornerPinNode['pin1'],
#                                                           cornerPinNode['pin2'],
#                                                           cornerPinNode['pin3'],
#                                                           cornerPinNode['pin4'])
#    except IOError as e:
#        nuke.message("Could not read file {0}:\n\nI/O error({1}): {2}".format(filename,e.errno, e.strerror))
#    except cornerPinData.FileFormatError as e:
#        nuke.message("Could not read file {0}:\n\nInvalid File Format: {1}".format(filename,e.message))

def loadTrackingDataFromFile():
    try:
        filename = nuke.getFilename('Load NUKE corner pin data from mocha', '*.nk')
        if filename is None:
            return
        cpData = cornerPinData.CornerPinDataFromNukeCornerPinFile(filename)
        applyTrackinData(cpData)
    except IOError as e:
        nuke.message("Could not read file {0}:\n\nI/O error({1}): {2}".format(filename, e.errno, e.strerror))
    except cornerPinData.FileFormatError as e:
        nuke.message("Could not read file {0}:\n\nInvalid File Format: {1}".format(filename, e.message))


def loadTrackinDataFromClipboard():
    try:
        cpData = cornerPinData.CornerPinDataFromClipboard()
        applyTrackinData(cpData)
    except cornerPinData.FileFormatError as e:
        nuke.message("Clipboard does not contain valid tracking data:\n{0}".format(e.message))


def applyTrackinData(cpData):
    cornerPinNode = nuke.thisNode()
    cornerPinKnobs.applyCornerPinDataToALlKnobs(cpData, cornerPinNode['pin1'],
                                                cornerPinNode['pin2'],
                                                cornerPinNode['pin3'],
                                                cornerPinNode['pin4'])

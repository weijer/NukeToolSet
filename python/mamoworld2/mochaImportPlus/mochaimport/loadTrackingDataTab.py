import nuke


def addLoadTrackingDataUI(trackerNode, commandLoadFromFile, commandLoadFromClipboard):
    trackerNode.addKnob(nuke.Tab_Knob('mochaImport', 'MochaImportPlus'))

    labelKnob = nuke.Text_Knob("loadMochaData", "load mocha tracking data")
    labelKnob.setFlag(nuke.STARTLINE)
    labelKnob.setTooltip("load mocha Nuke corner pin (*.nk) data")
    labelKnob.setValue('')
    trackerNode.addKnob(labelKnob)

    commandLoadFromFileWithChecks = addCheckToCommandWhetherMochaImportIsInstalled(commandLoadFromFile)
    loadDataFromFileKnob = nuke.PyScript_Knob("loadTrackingDataFromFile", "from file")
    loadDataFromFileKnob.setTooltip(
        "import mocha corner pin data from a file\n\nrequired format: Nuke Corner Pin (*.nk)")
    # loadDataFromFileKnob.setFlag(nuke.STARTLINE)
    loadDataFromFileKnob.setCommand(commandLoadFromFileWithChecks)
    trackerNode.addKnob(loadDataFromFileKnob)

    commandLoadFromClipboardWithChecks = addCheckToCommandWhetherMochaImportIsInstalled(commandLoadFromClipboard)
    loadDataFromClipboardKnob = nuke.PyScript_Knob("loadTrackingDataFromClipboard", "from clipboard")
    loadDataFromClipboardKnob.setTooltip(
        "import mocha corner pin data from the clipboard\n\nrequired format: Nuke Corner Pin (*.nk)")
    # loadDataFromClipboardKnob.setFlag(nuke.STARTLINE)
    loadDataFromClipboardKnob.setCommand(commandLoadFromClipboardWithChecks)
    trackerNode.addKnob(loadDataFromClipboardKnob)


def addCheckToCommandWhetherMochaImportIsInstalled(command):
    assert ('\n' not in command);  # command may not have multiple lines as this causes bad intendation in the result

    template = """ 
if not locals().__contains__("mochaimport"):
    nuke.message("Please install MochaImportPlus for NUKE (by mamoworld.com) to use this function")
else:
    {myCommand}
"""
    return template.format(myCommand=command)

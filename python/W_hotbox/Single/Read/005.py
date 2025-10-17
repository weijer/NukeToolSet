#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Version to...
#
#----------------------------------------------------------------------------------------------------------

import nukescripts

myKnobPanel = nuke.Panel('Set Version')
myKnobPanel.addSingleLineInput('Version','')

#show the panel
panel = myKnobPanel.show()

if panel:
    newVersion = myKnobPanel.value('Version')

    for i in nuke.selectedNodes():
        fileString = i.knob('file').value()
        curVersion = nukescripts.version_get(fileString, 'v')[-1]
        newVersion = newVersion.zfill(len(curVersion))
        i.knob('file').setValue(fileString.replace(curVersion,newVersion))

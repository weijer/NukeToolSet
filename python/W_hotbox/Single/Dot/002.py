#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Connect Left to Right
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

dict = {i.xpos():i for i in selection}
sortedKeys = sorted(dict.keys())

originalInput = dict[sortedKeys[-1]].input(0)

for i in selection:
    i.setInput(0,None)

for index, i in enumerate(sortedKeys):
    try:
        dict[i].setInput(0,dict[sortedKeys[index+1]])
    except:
        pass

if originalInput not in dict.values():
    dict[sortedKeys[-1]].setInput(0,originalInput)
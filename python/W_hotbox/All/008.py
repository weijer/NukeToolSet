#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Select Similar
#
#----------------------------------------------------------------------------------------------------------

def getGroupName(name):
    #strip name of numbers at the end
    while name[-1] in [str(i) for i in range(10)]:
            name = name[:-1]  

    return name
    
classesList = [[],[]]

#compose list of selected nodes
for i in nuke.selectedNodes():
    nodeClass = i.Class() 
    if nodeClass != 'Group' and nodeClass not in classesList:
        classesList[0].append(nodeClass)
    else:
        name = getGroupName(i.name())
        if name not in classesList:
            classesList[1].append(name)

#select all nodes
for i in nuke.allNodes():
    nodeClass = i.Class() 
    if nodeClass == 'Group':
        if getGroupName(i.name()) in classesList[1]:
            i.knob('selected').setValue(True)
    else:
        if nodeClass in classesList[0]:
            i.knob('selected').setValue(True)


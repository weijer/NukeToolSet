#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: ReformThat
#
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# January 2016
# v1.0
#----------------------------------------------------------------------------------------------------------
import nuke

def reformThat():
    '''
    Quickly set the format knob on a reformatnode to the format of an other node. If no reformat node is selected,
    a new one will be created.
    '''
    selection = nuke.selectedNodes()
    
    #if you've nothing selected you probably missclicked while trying to create a regular reformat
    #so I'll be nice and create a regular reformat for you anyway and do nothing else
    if len(selection) < 1:
        nuke.createNode('Reformat')
        return
    
    #if you selected a group of nodes, I'm not sure which node to steal the format from. So please try again
    if len(selection) > 2:
        nuke.message('please select only two nodes')
        return

    #if you've only one node selected, we have something to steal from but nothing to apply it to..
    #so create a new reformatnode
    
    reformatNode = ''
    
    if len(selection) == 1:
        selection[0].knob('selected').setValue(False)
        reformatNode = nuke.createNode('Reformat')
        
    #define the reformat node
    for i in selection:
        if i.Class() == 'Reformat' and reformatNode == '':
            reformatNode = i
            selection.remove(i)
            break
    
    #if none of the selected nodes is a reformat. Check the nodes for a format knob.
    #if one of the nodes happens to have one, use that node. 
    if len(selection) == 2:
        for i in selection[::-1]:
	    if i.Class() != 'Read' and 'format' in i.knobs():
	        reformatNode = i
                selection.remove(i)
                break
                
    #if you've multiple nodes selected at least one should be formatable. 
    #Otherwise we have plenty of selected sources to steal our formats from, but nowhere to store are just acquired treasures
    if len(selection) == 2:
        nuke.message('If you select multiple nodes, make sure at least one is a reformat or has an formatknob')
        return
        
    #define the node you want to match the format from
    targetNode = selection[0]
     
    #built a dictionary of all the existing formats in the scene
    formatsDict = {}
    for i in nuke.formats():
        if i.name() != None:
            formatsDict[(i.width(), i.height(),i.pixelAspect())]=i.name()

    targetFormat = (targetNode.format().width(), targetNode.format().height(), targetNode.format().pixelAspect())

    #check whether the format you're trying to copy already exists in your script
    if targetFormat in formatsDict:
        name = formatsDict[targetFormat]

    #if that's not the case, add it.
    else:
        name = 'custom 01'
        counter = 2
        while name in formatsDict.values():
            name = 'custom ' + str(counter).zfill(2)
            counter += 1

        nuke.addFormat(' '.join(map(str,targetFormat)) + ' ' + name)

    #set the reformatnode to new format
    reformatNode.knob('format').setValue(name)

reformThat()
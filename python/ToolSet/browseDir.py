# Browse Directory v1.0, 2011-11-12
# by Fredrik Averpil, fredrik.averpil [at] gmail.com, www.averpil.com/fredrik
# 
#
# Usage:
# a) select any Write node or Read node and run browseDirByNode()
# b) open any path via command browseDir(path)
# 
# Example of menu.py:
# import browseDir
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Node\'s file path', "browseDir.browseDirByNode()", 'shift+b' )
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('scripts')" )
#
# And if your folder structure looks like this -
# serverpath/ ... sequence_folder/shot_folder/nuke/scripts/
# you should be able to use the following as well:
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('sequence')" )
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('shot')" )
#
#



import nuke
import sys
import os
import re


def launch(directory):
    # Open folder
    print('Attempting to open folder: ' + directory)
    if os.path.exists(directory):
        if (sys.platform == 'win32'):
            os.system('start ' + directory)
        elif (sys.platform == 'darwin'):
            os.system('open ' + directory)
    else:
        nuke.message('Path does not exist:\n' + directory)


def browseDirByNode():
    error = False

    selectedNode = nuke.selectedNode()

    try:
        selectedNodeFilePath = nuke.callbacks.filenameFilter(selectedNode['file'].getValue())

    except ValueError:
        error = True
        nuke.message('No node selected.')
    except NameError:
        error = True
        nuke.message('You must select a Read node or a Write node.')

    if error == False:
        filePathSplitted = str.split(selectedNodeFilePath, '/')

    dirFromNode = ''
    for i in range(0, (len(filePathSplitted) - 1)):
        dirFromNode = dirFromNode + filePathSplitted[i] + '/'

    regcombile_r = re.compile('(//192.168.0.243/nas/)\S+')
    regcombile_t = re.compile('(//192.168.0.250/tvcServe/)\S+')
    matchgroup_r = regcombile_r.match(dirFromNode)
    matchgroup_t = regcombile_t.match(dirFromNode)
    print matchgroup_r, matchgroup_t

    if matchgroup_r:
        dirFromNode_new = re.sub("//192.168.0.243/nas/", "R:/", dirFromNode)
    elif matchgroup_t:
        dirFromNode_new = re.sub("//192.168.0.250/tvcServe/", "T:/", dirFromNode)
    else:
        dirFromNode_new = dirFromNode

    print dirFromNode
    # selectedNode['file'].setValue(dirFromNode_new)


    # Debug
    # print('Directory: ' + dirFromNode)

    launch(dirFromNode_new)

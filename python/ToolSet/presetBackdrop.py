# Preset Backdrop 1.2
# Copyright (c) 2011 Victor Perez.  All Rights Reserved.
### Add to menu.py ###
# import presetBackdrop
# VictorMenu = nuke.menu('Nuke').addMenu('V!ctor')
# VictorMenu.addCommand('Preset Backdrop', 'presetBackdrop.presetBackdrop()', 'ctrl+alt+b')
###

import nuke, colorsys, operator


### Preset Backdrop
def presetBackdrop():
    customPreset = None
    sep = '"'
    presets = ['Main', 'CG', 'Key', 'Output', 'Roto']
    p = nuke.Panel('Preset Backdrop')
    p.addEnumerationPulldown('Preset', ' '.join(presets))
    p.addSingleLineInput('Custom Label', '')
    if p.show():
        customPreset = p.value('Preset')
        customLabel = p.value('Custom Label')

    # Backdrop presets    
    if customPreset == 'Main':
        presetLabel = 'Main'
        presetIcon = 'Glint.png'
        presetColor = colorsys.hsv_to_rgb(0, 1, 0.5)

    elif customPreset == 'CG':
        presetLabel = 'CG'
        presetIcon = 'Shader.png'
        presetColor = colorsys.hsv_to_rgb(0.062, 1, 0.5)

    elif customPreset == 'Key':
        presetLabel = 'Key'
        presetIcon = 'Keyer.png'
        presetColor = colorsys.hsv_to_rgb(0.333, 1, 0.5)

    elif customPreset == 'Output':
        presetLabel = 'Output'
        presetIcon = 'Write.png'
        presetColor = colorsys.hsv_to_rgb(0.167, 1, 0.373)

    elif customPreset == 'Roto':
        presetLabel = 'Roto'
        presetIcon = 'Roto.png'
        presetColor = colorsys.hsv_to_rgb(0.333, 0.430, 0.384)

    ### Backdrop creation based on presets
    if customPreset is not None:
        # RGB to HEX
        r = presetColor[0]
        g = presetColor[1]
        b = presetColor[2]
        hexColour = int('%02x%02x%02x%02x' % (r * 255, g * 255, b * 255, 1), 16)

        if presetIcon == '':
            icon = ''
        else:
            icon = '<img src=' + sep + presetIcon + sep + '> '

        selNodes = nuke.selectedNodes()
        if not selNodes:
            if customLabel == '':
                return nuke.nodes.BackdropNode(label='<center>' + icon + presetLabel, tile_color=hexColour,
                                               note_font_size=30)
            else:
                return nuke.nodes.BackdropNode(label='<center>' + icon + customLabel, tile_color=hexColour,
                                               note_font_size=30)

        # Find Min. and Max. of Positions
        positions = [(i.xpos(), i.ypos()) for i in selNodes]
        xPos = sorted(positions, key=operator.itemgetter(0))
        yPos = sorted(positions, key=operator.itemgetter(1))
        xMinMaxPos = (xPos[0][0], xPos[-1:][0][0])
        yMinMaxPos = (yPos[0][1], yPos[-1:][0][1])

        if customLabel == '':
            n = nuke.nodes.BackdropNode(xpos=xMinMaxPos[0] - 10, bdwidth=xMinMaxPos[1] - xMinMaxPos[0] + 110,
                                        ypos=yMinMaxPos[0] - 85, bdheight=yMinMaxPos[1] - yMinMaxPos[0] + 160,
                                        label='<center>' + icon + presetLabel, tile_color=hexColour, note_font_size=30)
        else:
            n = nuke.nodes.BackdropNode(xpos=xMinMaxPos[0] - 10, bdwidth=xMinMaxPos[1] - xMinMaxPos[0] + 110,
                                        ypos=yMinMaxPos[0] - 85, bdheight=yMinMaxPos[1] - yMinMaxPos[0] + 160,
                                        label='<center>' + icon + customLabel, tile_color=hexColour, note_font_size=30)

        n['selected'].setValue(False)

        # Revert to Previous Selection
        [i['selected'].setValue(True) for i in selNodes]

        return n
    else:
        pass

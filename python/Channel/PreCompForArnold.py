import nuke


def preCompForArnold():
    # set a ordered list of input layer
    layerlist = ['indirect_diffuse', 'direct_diffuse', 'indirect_specular', 'direct_specular', 'reflection',
                 'refraction',
                 'AO', 'depth', 'MV', 'alpha']
    gradelayers = ['indirect_diffuse', 'direct_diffuse', 'indirect_specular', 'direct_specular', 'reflection',
                   'refraction',
                   'AO']
    # Get The Layers Of Selected Read Node

    orderedmerge = []

    Read = nuke.selectedNode()
    layers = nuke.layers(Read)

    for i in layerlist:
        for n in layers:
            if i == n:
                orderedmerge.append(i)

    for o in orderedmerge:
        for l in layers:
            if l == o:
                layers.remove(l)

    layers.remove('rgba')
    layers.remove('rgb')
    orderedshow = layers

    ################Create Shuffle########################################

    x = Read['xpos'].getValue()
    y = Read['ypos'].getValue()

    shufflegroup = []
    gradegroup = []
    dotYgroup = []
    mergegroup = []
    for k in orderedmerge:
        shuffle = nuke.nodes.Shuffle(name=k, postage_stamp=1, note_font_size=25)
        shuffle.setInput(0, Read)
        shuffle.knob('in').setValue(k)
        num = int(orderedmerge.index(k))
        shuffle.setXYpos(int(x + 150 * num), int(y + 250))
        shuffleX = shuffle['xpos'].getValue()
        shuffleY = shuffle['ypos'].getValue()
        shufflegroup.append(shuffle)

        ###Create Grade###
        if num < 7:
            gradenode = nuke.nodes.Grade(name=k, note_font_size=15)
            gradenode.setInput(0, shuffle)
            gradegroup.append(gradenode)
        else:
            pass

        ###Create Dot#####

        if num >= 1 and num < 7:
            dot = nuke.nodes.Dot(name=k, label=k, note_font_size=25)
            dot.setInput(0, gradenode)
            dot.setXYpos(int(shuffleX + 34), int(shuffleY + 180 * num))
            dotX = dot['xpos'].getValue()
            dotY = dot['ypos'].getValue()
            dotYgroup.append(dotY)

        elif num > 6:
            dot = nuke.nodes.Dot(name=k, label=k, note_font_size=25)
            dot.setInput(0, shuffle)
            dot.setXYpos(int(shuffleX + 34), int(shuffleY + 180 * num))
            dotX = dot['xpos'].getValue()
            dotY = dot['ypos'].getValue()
            dotYgroup.append(dotY)

        ###Create Merge####

        if num < 1:
            pass
        elif num > 0 and num < 2:
            merge = nuke.nodes.Merge(name=k, operation='plus', mix=1, inputs=[gradegroup[0], dot], note_font_size=15)
            merge.setXYpos(int(x), int(dotY - 6))
            mergegroup.append(merge)
        elif num > 1 and num < 6:
            merge = nuke.nodes.Merge(name=k, operation='plus', mix=1, inputs=[mergegroup[num - 2], dot],
                                     note_font_size=15)
            mergegroup.append(merge)
            merge.setXYpos(int(x), int(dotY - 6))
        elif num > 5 and num < 7:
            merge = nuke.nodes.Merge(name=k, operation='multiply', mix=0.15, inputs=[mergegroup[num - 2], dot],
                                     note_font_size=15)
            mergegroup.append(merge)
            merge.setXYpos(int(x), int(dotY - 6))
        elif num > 6 and num < 8:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='depth.Z', inputs=[mergegroup[num - 2], dot],
                                   note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 14))
        elif num > 7 and num < 9:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='MV.red', from1='rgba.green', to1='MV.green',
                                   inputs=[mergegroup[num - 2], dot], note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 26))
        elif num > 8 and num < 10:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='rgba.alpha', inputs=[mergegroup[num - 2], dot],
                                   note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 14))
            ###Create show Layers####

    for element in orderedshow:
        num += 1
        shuffle = nuke.nodes.Shuffle(name=element, postage_stamp=1, note_font_size=25)
        shuffle.setInput(0, Read)
        shuffle.knob('in').setValue(element)
        shuffle.setXYpos(int(x + 150 * num), int(y + 250))

    nuke.connectViewer(0, mergegroup[-1])

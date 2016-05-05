import nuke


def shuffle():
    for selected_node in nuke.selectedNodes():
        if selected_node.Class() == 'Read':
            all_channels = selected_node.channels()
            all_channels = list(set([i.split('.')[0] for i in all_channels]))
            for channel in all_channels:
                shuffle_node = nuke.createNode('Shuffle', inpanel=False)
                shuffle_node['name'].setValue(channel+'_'+selected_node['name'].getValue())
                shuffle_node['in'].setValue(channel)
                shuffle_node.setInput(0, selected_node)
                shuffle_node['postage_stamp'].setValue(1)


def main():
    shuffle()
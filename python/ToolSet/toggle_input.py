# -*- coding: utf-8 -*-
import nuke


def toggleInput():
    sel = nuke.selectedNodes()
    if len(sel):
        toggleVal = not bool(sel[0].knob('hide_input').getValue())
        for node in sel:
            if node.knob('hide_input') != None:
                node.knob('hide_input').setValue(toggleVal)
    else:
        nodes = nuke.allNodes()
        toggleVal = not bool(nodes[0].knob('hide_input').getValue())
        for node in nodes:
            if node.knob('hide_input') != None:
                node.knob('hide_input').setValue(toggleVal)


def main():
    toggleInput()

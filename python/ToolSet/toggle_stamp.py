# -*- coding: utf-8 -*-
import nuke


def toggleStamp():
    sel = nuke.selectedNodes()
    if len(sel):
        toggleVal = True
        for n in sel:
            if n.knob('postage_stamp') != None:
                toggleVal = not bool(n.knob('postage_stamp').getValue())
                break
        for node in sel:
            if node.knob('postage_stamp') != None:
                node.knob('postage_stamp').setValue(toggleVal)
    else:
        nodes = nuke.allNodes()
        toggleVal = True
        for n in nodes:
            if n.knob('postage_stamp') != None:
                toggleVal = not bool(n.knob('postage_stamp').getValue())
                break
        for node in nodes:
            if node.knob('postage_stamp') != None:
                node.knob('postage_stamp').setValue(toggleVal)

def main():
    toggleStamp()

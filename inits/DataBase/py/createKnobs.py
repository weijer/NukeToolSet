# Author: Wang Chenxu
# Last Edit: Wang Chenxu
# Started Date: 2024-10-26 00:45:09
# Last edited: 2024-10-26 12:03:44

import addOptions
import nuke

def get_all_knob_names(node):
    # get all knobs from the DataBase node
    return [n for n in node.knobs()]


def get_knob_name_set(node):
    # get all knob names from the DataBase node's "knobNameSet" knobs
    return node['knobNameSet'].getValue()


def create_int_knob():
    # create integer knob with clicking on this button
    n = nuke.thisNode()
    knob_name = nuke.getInput('knob name:')

    if not knob_name is None:
        if not knob_name in get_all_knob_names(n):
            k = nuke.Int_Knob(knob_name)
            n.addKnob(k)
            if not knob_name in get_knob_name_set(n):
                ori_knob_name_set = str(n['knobNameSet'].getValue())
                ori_knob_name_set += ' ' + knob_name
                n['knobNameSet'].setValue(ori_knob_name_set)
        else:
            nuke.message("knob name \"{0}\" already exists".format(knob_name))
        addOptions.update_options()


def create_float_knob():
    # Create float knob with clicking on this button
    n = nuke.thisNode()
    knob_name = nuke.getInput('knob name:')

    if not knob_name is None:
        if not knob_name in get_all_knob_names(n):
            k = nuke.Double_Knob(knob_name)
            n.addKnob(k)
            if not knob_name in get_knob_name_set(n):
                ori_knob_name_set = str(n['knobNameSet'].getValue())
                ori_knob_name_set += ' ' + knob_name
                n['knobNameSet'].setValue(ori_knob_name_set)
        else:
            nuke.message("knob name \"{0}\" already exists".format(knob_name))
        addOptions.update_options()


def create_color_knob():
    # create color knob with clicking on this button
    n = nuke.thisNode()
    knob_name = nuke.getInput('knob name:')

    if not knob_name is None:
        if not knob_name in get_all_knob_names(n):
            k = nuke.Color_Knob(knob_name)
            n.addKnob(k)
            if not knob_name in get_knob_name_set(n):
                ori_knob_name_set = str(n['knobNameSet'].getValue())
                ori_knob_name_set += ' ' + knob_name
                n['knobNameSet'].setValue(ori_knob_name_set)
        else:
            nuke.message("knob name \"{0}\" already exists".format(knob_name))
        addOptions.update_options()


def clean_all():
    # clean up all knobs from the current node

    p = nuke.ask("Are you sure you want to clean all of it?")

    if p:
        n = nuke.thisNode()
        knob_name_set = get_knob_name_set(n)
        for k in n.knobs():
            if k in knob_name_set:
                n.removeKnob(n.knob(k))

        n['knobNameSet'].setValue('')

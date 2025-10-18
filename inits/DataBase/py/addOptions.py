# Author: Wang Chenxu
# Last Edit: Wang Chenxu
# Started Date: 2024-10-26 00:45:09
# Last edited: 2024-10-26 00:45:09


import nuke


def get_DataBase_node():
    # find DataBase node in node group, if not found return 0, if found return the node
    tn = nuke.thisNode()
    if tn.Class() == "Group":
        nuke.thisNode().end()
    nodeName = 'DataBase'
    for n in nuke.allNodes('Group'):
        if n.name() == nodeName:
            return n
    return 0


def update_options():
    # add options to the DataBase menu
    DataBase_node = get_DataBase_node()

    # check if DataBase node exists, if not, give a warning to the user
    # if yes, update the database options by clean and recreate the menu
    if not DataBase_node == 0:
        knob_name_set = DataBase_node['knobNameSet'].getValue()[1::]
        options = knob_name_set.split(' ')

        m = nuke.menu('Animation')
        mm = m.findItem("DataBase")
        mm.clearMenu()

        # this is for recreate "update" option after clear the DataBase Menu
        # even it's inside of python file, it will execute like when you execute it in nuke's script editor
        # so we need to reimport the file
        mm.addCommand("update", "import addOptions\naddOptions.update_options()")

        # if user select one of the options, then set expressions to link the knob to the parameter on DataBase node
        for option in options:
            mm.addCommand(option, "nuke.thisKnob().setExpression('DataBase.' + '{0}', 0)".format(option))

    else:
        nuke.message("You need to create a DataBase node first!")

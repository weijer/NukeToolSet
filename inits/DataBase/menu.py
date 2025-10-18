# Author: Wang Chenxu
# Last Edit: Wang Chenxu
# Started Date: 2024-10-26 00:45:09
# Last edited: 2024-10-26 00:45:09

import nuke
nuke.pluginAddPath('./py')

import addOptions


m = nuke.menu('Animation')
m.addCommand("DataBase/update", "addOptions.update_options()")

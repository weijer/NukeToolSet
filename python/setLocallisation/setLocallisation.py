# coding=utf-8
# author=weijer
# http://www.cgspread.com

import nuke


class Locallisation(object):
    def __init__(self):
        self._read_list = ['Read', 'ReadGeo2', 'Camera2', 'SmartVector', 'DeepRead']

    def selectNodes(self):
        selectNodes = nuke.selectedNodes()
        if selectNodes:
            self.upLocalizationPolicy(selectNodes)
        else:
            nuke.message("请选择节点")

    def upLocalizationPolicy(self, Nodes):
        for nodes in Nodes:
            if nodes.Class() in self._read_list:
                isEnabled = nuke.localisationEnabled(nodes.knob("localizationPolicy"))
                if not isEnabled:
                    nodes.knob("localizationPolicy").setValue(0)



run = Locallisation()
run.selectNodes()

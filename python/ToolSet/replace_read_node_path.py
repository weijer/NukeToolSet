#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/7
# version     :
# usage       :
# notes       :

# Built-in modules
from Qt import QtWidgets as QtGui
from Qt import QtCore as QtCore
# Third-party modules
import nuke
# Studio modules

# Local modules


class ReplacePath(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ReplacePath, self).__init__(parent)
        self.resize(500, 100)
        self.setWindowTitle('Replace Read Node Path')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(15)

        source_label = QtGui.QLabel('Source Path')
        self.source_le = QtGui.QLineEdit()
        target_label = QtGui.QLabel('Target Path')
        self.target_le = QtGui.QLineEdit()
        self.replace_btn = QtGui.QPushButton('Replace')
        self.replace_btn.clicked.connect(self.do_replace)

        source_layout = QtGui.QHBoxLayout()
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_le)

        target_layout = QtGui.QHBoxLayout()
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_le)

        main_layout.addLayout(source_layout)
        main_layout.addLayout(target_layout)
        main_layout.addWidget(self.replace_btn)

    def do_replace(self):
        source_path = str(self.source_le.text())
        target_path = str(self.target_le.text())
        for node in nuke.allNodes('Read'):
            node_file_path = node['file'].getValue()
            if source_path in node_file_path:
                new_path = node_file_path.replace(source_path, target_path)
                node['file'].setValue(new_path)


def main():
    app = QtGui.qApp
    global rp
    try:
        rp.close()
        rp.deleteLater()
    except:pass
    nuke_win = app.activeWindow()
    rp = ReplacePath(nuke_win)
    rp.show()

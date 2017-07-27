#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/9
# version     :
# usage       :
# notes       :

# Built-in modules
from Qt import QtWidgets as QtGui
from Qt import QtCore as QtCore
import os
import getpass
import re

import random
# Third-party modules
import nuke
# Studio modules

# Local modules
from libs import json_operation


class Nuke(object):

    def get_frames_under_sequence(self, sequence_dir):
        all_frames = os.listdir(sequence_dir)
        if 'Thumb.db' in all_frames:
            all_frames.remove('Thumb.db')
        if not all_frames:
            return
        all_frames = [frame for frame in all_frames
                      if os.path.isfile(os.path.join(sequence_dir, frame))]
        return all_frames

    def get_frame_range(self, sequence_dir, sep):
        all_frames = self.get_frames_under_sequence(sequence_dir)
        if all_frames:
            if sep == '.':
                pattern_frame = r'.*\.(\d+)\.(exr|png|jpg|jpeg|tga|tiff|tif|iff)'
            elif sep == '_':
                pattern_frame = r'.*_(\d+)\.(exr|png|jpg|jpeg|tga|tiff|tif|iff)'
            frame_numbers = [int(re.match(pattern_frame, frame).group(1))
                             for frame in all_frames
                             if re.match(pattern_frame, frame)]
            frame_numbers = list(set(frame_numbers))
            if frame_numbers:
                start_frame, end_frame = [min(frame_numbers), max(frame_numbers)]
                if len(frame_numbers) != end_frame - start_frame + 1:
                    nuke.message('%s has some frame lost' % os.path.basename(sequence_dir))
                return start_frame, end_frame
            else:
                return None, None, None
        else:
            return None, None, None

    def get_frame_profile(self, sequence_dir, sep):
        all_frames = self.get_frames_under_sequence(sequence_dir)
        if not all_frames:
            return
        if sep == '.':
            pattern_string = r'.*\.(\d+)\.(exr|png|jpg|jpeg|tga|tiff|tif|iff)'
        elif sep == '_':
            pattern_string = r'.*_(\d+)\.(exr|png|jpg|jpeg|tga|tiff|tif|iff)'
        matched = re.findall(pattern_string, all_frames[0])
        if len(all_frames) == 1:
            replaced_frame = all_frames[0]
        elif len(all_frames) > 1 and matched:
            if not matched[0][0].startswith('0'):
                replaced = '%d'
            else:
                replaced = '%0{num}d'.format(num=len(matched[0][0]))
            if sep == '.':
                replaced_frame = re.sub('\.(\d+)\.', '.'+replaced+'.', all_frames[0])
            elif sep == '_':
                replaced_frame = re.sub('_(\d+)\.', '_'+replaced+'.', all_frames[0])
        return os.path.join(sequence_dir, replaced_frame).replace('\\', '/')

    def fix_read_node(self, read_node, start_frame, end_frame):
        read_node['first'].setValue(start_frame)
        read_node['last'].setValue(end_frame)
        read_node['origfirst'].setValue(start_frame)
        read_node['origlast'].setValue(end_frame)
        read_node['label'].setValue("<font size=\"4\" color =#548DD4><b> Frame range :</b></font>"
                                    " <font color = red>[value first] - [value last] </font>")

    def import_pictures(self, sequence_dir, sep):
        all_read_file = [read_node['file'].getValue()
                         for read_node in nuke.allNodes('Read')]
        all_read_file = list(set(all_read_file))
        start_frame, end_frame = self.get_frame_range(sequence_dir, sep)
        read_file_name = self.get_frame_profile(sequence_dir, sep)
        if read_file_name:
            read_file_name = read_file_name.replace('\\', '/')
        if all((start_frame, end_frame)) and read_file_name not in all_read_file:
            read_node = nuke.nodes.Read(file=read_file_name)
            self.fix_read_node(read_node, start_frame, end_frame)
            nuke.zoom(1, [read_node.xpos(), read_node.ypos()])

    def import_project_pictures(self, project_dir, sep):
        if os.path.isdir(project_dir):
            sequence_dirs = [os.path.join(project_dir, sequence_dir).replace('\\', '/')
                             for sequence_dir in os.listdir(project_dir)
                             if os.path.isdir(os.path.join(project_dir, sequence_dir))]
            if sequence_dirs:
                task = nuke.ProgressTask("AAS | Reading Files")
                value = 1
                for sequence_dir in sequence_dirs:
                    task.setMessage(sequence_dir)
                    task.setProgress(100/len(sequence_dirs)*value)
                    try:
                        self.import_pictures(sequence_dir, sep)
                    except Exception as e:
                        print '[AAs] error:', e
                    value += 1
                task.setMessage('Auto Read Successful')
                task.setProgress(100)
        else:
            print '[AAS info]: %s is not an exist folder' % project_dir

    def get_current_shot_options(self):
        all_paths = list()
        for read_node in nuke.allNodes('Read'):
            file_name = read_node['file'].getValue()
            file_dir_name = os.path.dirname(file_name)
            all_path = file_dir_name.split('/')
            all_paths.extend(all_path)
        all_paths = list(set(all_paths))
        current_shot = [content for content in all_paths
                        if re.findall('\d+', content)]
        return current_shot

    def get_current_project_dir(self):
        all_dirs = list()
        if not nuke.allNodes('Read'):
            return
        for read_node in nuke.allNodes('Read'):
            file_name = read_node['file'].getValue()
            file_dir_name = os.path.dirname(os.path.dirname(file_name))
            all_dirs.append(file_dir_name)
        all_dirs = list(set(all_dirs))
        return all_dirs

    def replace_shot(self, current_shot, new_shot, sep):
        all_read_node = nuke.allNodes('Read')
        if all_read_node:
            replace_task = nuke.ProgressTask("AAS | Replacing Files")
            value = 1
            for read_node in nuke.allNodes('Read'):
                replace_task.setProgress(100/len(all_read_node)*value)
                file_name = read_node['file'].getValue()
                new_file_name = re.sub(current_shot, new_shot, file_name)
                new_file_dir = os.path.dirname(new_file_name)
                if os.path.isdir(new_file_dir):
                    read_node['file'].setValue(self.get_frame_profile(new_file_dir, sep))
                    read_node['disable'].setValue(0)
                    start_frame, end_frame = self.get_frame_range(new_file_dir, sep)
                    self.fix_read_node(read_node, start_frame, end_frame)
                else:
                    read_node['disable'].setValue(1)
                value += 1
            replace_task.setProgress(100)

    def show_message(self, message):
        nuke.message(message)


class ReplaceReadNodeView(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ReplaceReadNodeView, self).__init__(parent)
        self.setWindowTitle('Replace Read Node')
        self.resize(550, 120)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(5, 15, 5, 10)

        file_path_layout = QtGui.QHBoxLayout()
        file_path_label = QtGui.QLabel('The File Path')
        file_path_label.setAlignment(QtCore.Qt.AlignVCenter)
        file_path_label.setFixedWidth(80)
        file_path_label.setAlignment(QtCore.Qt.AlignRight)
        self.file_path_cbox = QtGui.QComboBox()
        self.file_path_cbox.setEditable(True)
        self.file_path_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.file_path_btn.setIcon(icon)
        separator_label = QtGui.QLabel('Sep:')
        separator_label.setFixedWidth(30)
        self.separator_cbox = QtGui.QComboBox()
        self.separator_cbox.setFixedWidth(30)
        for separator in ['.', '_']:
            self.separator_cbox.addItem(separator)
        self.import_btn = QtGui.QPushButton('Import')
        self.import_btn.setFixedWidth(75)

        file_path_layout.addWidget(file_path_label)
        file_path_layout.addWidget(self.file_path_cbox)
        file_path_layout.addWidget(self.file_path_btn)
        file_path_layout.addWidget(separator_label)
        file_path_layout.addWidget(self.separator_cbox)
        file_path_layout.addWidget(self.import_btn)

        replace_grp = QtGui.QGroupBox('Replace')
        replace_layout = QtGui.QHBoxLayout(replace_grp)
        replace_layout.setContentsMargins(10, 15, 10, 15)
        shot_attr_layout = QtGui.QVBoxLayout()
        shot_attr_layout.setSpacing(20)
        current_shot_layout = QtGui.QHBoxLayout()
        current_shot_layout.setSpacing(3)
        current_shot_label = QtGui.QLabel('Current scene/shot no.')
        current_shot_label.setFixedWidth(130)
        current_shot_label.setAlignment(QtCore.Qt.AlignRight)
        self.current_shot_cbox = QtGui.QComboBox()
        self.current_shot_cbox.setEditable(True)
        current_shot_layout.addWidget(current_shot_label)
        current_shot_layout.addWidget(self.current_shot_cbox)
        new_shot_layout = QtGui.QHBoxLayout()
        new_shot_layout.setSpacing(3)
        new_shot_label = QtGui.QLabel('New scene/shot no.')
        new_shot_label.setFixedWidth(130)
        new_shot_label.setAlignment(QtCore.Qt.AlignRight)
        self.new_shot_le = QtGui.QLineEdit()
        new_shot_layout.addWidget(new_shot_label)
        new_shot_layout.addWidget(self.new_shot_le)

        shot_attr_layout.addLayout(current_shot_layout)
        shot_attr_layout.addLayout(new_shot_layout)

        self.replace_btn = QtGui.QPushButton('Replace')
        self.replace_btn.setFixedSize(75, 62)

        replace_layout.addLayout(shot_attr_layout)
        replace_layout.addWidget(self.replace_btn)

        button_layout = QtGui.QHBoxLayout()
        self.replace_and_import_btn = QtGui.QPushButton('Replace And Import')
        button_layout.addStretch()
        button_layout.addWidget(self.replace_and_import_btn)
        main_layout.addLayout(file_path_layout)
        main_layout.addWidget(replace_grp)
        main_layout.addLayout(button_layout)


class ReplaceReadNode(ReplaceReadNodeView):
    nuke_util = Nuke()

    def __init__(self, parent=None):
        super(ReplaceReadNode, self).__init__(parent)
        self.init_shot()
        self.init_file_path()
        self.set_signals()

    def init_shot(self):
        current_shot_options = self.nuke_util.get_current_shot_options()
        self.current_shot_cbox.addItems(current_shot_options)
        if current_shot_options:
            self.current_shot_cbox.setCurrentIndex(self.current_shot_cbox.findText(current_shot_options[0]))
        self.new_shot_le.setText(self.current_shot_cbox.itemText(0))

    def init_file_path(self):
        project_dirs = self.nuke_util.get_current_project_dir()
        if project_dirs:
            self.file_path_cbox.addItems(project_dirs)

    def set_signals(self):
        self.file_path_btn.clicked.connect(self.choose_file_path)
        self.file_path_cbox.currentIndexChanged.connect(self.save_history)
        self.file_path_cbox.editTextChanged.connect(self.save_history)
        self.import_btn.clicked.connect(self.do_import)
        self.current_shot_cbox.currentIndexChanged.connect(self.set_new_shot)
        self.replace_btn.clicked.connect(self.do_replace)
        self.replace_and_import_btn.clicked.connect(self.replace_and_import)

    def choose_file_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        current_text = self.file_path_cbox.currentText()
        if current_text:
            caption = os.path.dirname(current_text)
        else:
            caption = '/'
        file_path = file_dialog.getExistingDirectory(self, 'choose directory', caption)
        if file_path:
            file_path = file_path.replace('\\', '/')
            if self.file_path_cbox.findText(file_path) == -1:
                self.file_path_cbox.addItem(str(file_path))
                self.file_path_cbox.setCurrentIndex(self.file_path_cbox.findText(file_path))

    def get_history_path(self):
        user = getpass.getuser()
        nuke_root_path = 'C:/Users/%s/.nuke' % user
        history_dir = os.path.join(nuke_root_path, 'history')
        history_path = os.path.join(history_dir, 'replace_read_node.json')
        return history_path

    def set_new_shot(self, index):
        if not self.new_shot_le.text():
            current_shot = self.current_shot_cbox.itemText(index)
            self.new_shot_le.setText(current_shot)

    def save_history(self, value):
        history_path = self.get_history_path()
        history_dir = os.path.dirname(history_path)
        if not os.path.isdir(history_dir):
            os.makedirs(history_dir)
        if isinstance(value, int):
            text = self.file_path_cbox.itemText(value)
        else:
            text = str(value)
        if text:
            json_operation.set_json_data(history_path, {"history": text})

    def do_import(self):
        picture_dir = str(self.file_path_cbox.currentText())
        sep = str(self.separator_cbox.currentText())
        self.nuke_util.import_project_pictures(picture_dir, sep)
        self.init_shot()

    def read_settings(self):
        history_path = self.get_history_path()
        if not os.path.isfile(history_path):
            return
        history_info = json_operation.get_json_data(history_path)
        if self.file_path_cbox.findText(str(history_info['history'])) == -1:
            self.file_path_cbox.addItem(str(history_info['history']))

    def do_replace(self):
        current_shot = str(self.current_shot_cbox.currentText())
        new_shot = str(self.new_shot_le.text())
        sep = str(self.separator_cbox.currentText())
        if current_shot != new_shot:
            self.nuke_util.replace_shot(current_shot, new_shot, sep)

    def replace_and_import(self):
        self.do_replace()
        picture_dir = str(self.file_path_cbox.currentText())
        current_shot = str(self.current_shot_cbox.currentText())
        new_shot = str(self.new_shot_le.text())
        new_dir = re.sub(current_shot, new_shot, picture_dir)
        sep = str(self.separator_cbox.currentText())
        if current_shot in picture_dir:
            self.nuke_util.import_project_pictures(new_dir, sep)
        else:
            self.nuke_util.show_message('[AAS info]: Perhaps \n %s \n is not the'
                                        'directory what you want to import.' % new_dir)


def main():
    app = QtGui.qApp
    global rrn
    try:
        rrn.close()
        rrn.deleteLater()
    except:pass
    nuke_win = app.activeWindow()
    rrn = ReplaceReadNode(nuke_win)
    rrn.read_settings()
    rrn.show()

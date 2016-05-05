# coding=utf-8
# author=weijer
import nuke
import os.path
import shutil
import re
import config


class Package(object):
    def __init__(self, target_dir, Progress_Main=None, show_Progress=None):
        self._read_list = ['Read', 'ReadGeo2', 'Camera2', 'SmartVector', 'DeepRead']
        self.target_dir = target_dir
        self.Progress_Main = Progress_Main
        self.show_Progress = show_Progress
        self.config = config.config
        self.m_dir = self.config["m_dir"]
        self.p_dir = self.config["p_dir"]
        self.g_dir = self.config["g_dir"]
        self._relative_path = '[python {nuke.script_directory()}]'

        # current project path
        current_project = nuke.Root().name()
        proj_path = os.path.splitext(current_project)
        self._nuke_proj = current_project
        self._proj_name = (os.path.split(proj_path[0]))[1]
        self._proj_basename = os.path.basename(current_project)
        self._proj_path = os.path.dirname(current_project)

    def packed_file(self):
        """
        Package nuke project
        :return:
        """
        # backup project
        # backup_name = self._proj_name + "_backup.nk"
        # backup_path = os.path.join(self._proj_path, backup_name)
        # shutil.copy(self._nuke_proj, backup_path)

        # packed project
        allNodes = nuke.allNodes()
        maxlen = len(allNodes)
        start_len = 0

        # set progressDialog range
        progressDialog = self.show_Progress
        progressDialog.setRange(1, maxlen)

        for node in allNodes:
            start_len += start_len
            node_class = node.Class()
            if node_class in self._read_list:
                read_file = node.knob("file").getValue()
                file_info = self.get_file_path(read_file)
                if file_info:
                    # copy dir option
                    copy_dirname = ""
                    if file_info["suffix"] in self.config["m_suffix"]:
                        copy_dirname = self.config["m_dir"]
                    elif file_info["suffix"] in self.config["p_suffix"]:
                        copy_dirname = self.config["p_dir"]
                    elif file_info["suffix"] in self.config["g_suffix"]:
                        copy_dirname = self.config["g_dir"]
                    copy_dir = os.path.join(self.target_dir, copy_dirname)
                    # is sequence copy dir
                    if file_info["is_sequence"]:
                        copy_path = os.path.join(copy_dir, file_info["folder"])
                        relative_folder = os.path.join(self._relative_path, copy_dirname)
                        relative_dir = os.path.join(relative_folder, file_info["folder"])
                        # Multiple nodes refer to the same material
                        if not os.path.isdir(copy_path):
                            shutil.copytree(file_info["dir_name"], copy_path)

                    # is file copy file
                    else:
                        copy_path = os.path.join(copy_dir, file_info["base_name"])
                        relative_dir = os.path.join(self._relative_path, copy_dirname)
                        if not os.path.isdir(copy_dir):
                            os.makedirs(copy_dir)
                        shutil.copy2(read_file, copy_path)

                    print copy_path
                    # change file path to relative
                    cdir = os.path.join(relative_dir, file_info["base_name"])
                    cdir = cdir.replace("\\", "/")
                    node.knob("file").setValue(cdir)

            # set progressDialog value
            progressDialog.setValue(start_len)

        # save as nuke script project
        project_path = os.path.join(self.target_dir, self._proj_basename)
        nuke.scriptSaveAs(project_path, 1)
        self.Progress_Main.close()

    def get_file_path(self, path):
        """
        Get file info
        :param path:
        :return: file dict
        """
        if path:
            suffix = os.path.splitext(path)[1]
            base_name = os.path.basename(path)
            dir_name = os.path.dirname(path)
            folder = os.path.split(dir_name)[1]
            is_sequence = self.check_sequence(base_name)
            path_dict = {
                "suffix": suffix,
                "base_name": base_name,
                "dir_name": dir_name,
                "folder": folder,
                "is_sequence": is_sequence
            }
            return path_dict
        else:
            return

    def check_sequence(self, basename):
        """
        To determine whether the sequence

        :param basename:
        :return: bool
        """
        rex = '(%\d+d|#+)'
        if re.search(rex, basename):
            # result = re.search(rex, basename)
            return True
        else:
            return False

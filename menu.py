# coding=utf-8
# author=weijer
# http://www.cgspread.com

import nuke
import os.path
import config
import sys
import command
import mochaimport


class NukeMenu(object):
    def __init__(self):
        self.config = config.nuke_config

        """
        get current nuke version number
        """
        self.nuke_version_number = nuke.NUKE_VERSION_MAJOR

        """
         add folder path
        """
        base_dir = os.path.dirname(__file__)
        self.root_base_dir = base_dir
        self.libs_dir = self.replace_path(os.path.join(base_dir, "libs"))
        self.luts_dir = self.replace_path(os.path.join(base_dir, "luts"))
        self.python_dir = self.replace_path(os.path.join(base_dir, "python"))
        self.template_dir = self.replace_path(os.path.join(base_dir, "template"))

        """
         add default init
        """
        self.default_init()

        """
         append system path
        """
        if not self.python_dir in sys.path:
            sys.path.append(self.python_dir)

        """
         add gizmos path
        """
        self.gizmos_image_dir = self.replace_path(os.path.join(base_dir, "gizmos/Image"))
        self.gizmos_Filter_dir = self.replace_path(os.path.join(base_dir, "gizmos/Filter"))
        self.gizmos_channel_dir = self.replace_path(os.path.join(base_dir, "gizmos/Channel"))
        self.gizmos_Lighting_dir = self.replace_path(os.path.join(base_dir, "gizmos/Lighting"))
        self.gizmos_3D_dir = self.replace_path(os.path.join(base_dir, "gizmos/3D"))
        self.gizmos_Keyer_dir = self.replace_path(os.path.join(base_dir, "gizmos/Keyer"))
        self.gizmos_ToolSet_dir = self.replace_path(os.path.join(base_dir, "gizmos/ToolSet"))
        self.gizmos_3D_Tangent_dir = self.replace_path(os.path.join(base_dir, "gizmos/3D/Tangent_Space_Normals"))
        nuke.pluginAddPath(self.gizmos_image_dir)
        nuke.pluginAddPath(self.gizmos_Filter_dir)
        nuke.pluginAddPath(self.gizmos_channel_dir)
        nuke.pluginAddPath(self.gizmos_Lighting_dir)
        nuke.pluginAddPath(self.gizmos_3D_dir)
        nuke.pluginAddPath(self.gizmos_Keyer_dir)
        nuke.pluginAddPath(self.gizmos_ToolSet_dir)
        nuke.pluginAddPath(self.gizmos_3D_Tangent_dir)

        """
        add Cryptomatte gizmo path
        """
        if self.nuke_version_number < 13:
            self.gizmos_cryptomatte_dir = self.replace_path(os.path.join(base_dir, "gizmos/Cryptomatte"))
            nuke.pluginAddPath(self.gizmos_cryptomatte_dir)

        """
         add icons path
        """
        self.icons_menu_dir = self.replace_path(os.path.join(base_dir, "icons/icon_menu"))
        self.icons_toolbar_dir = self.replace_path(os.path.join(base_dir, "icons/icon_toolbar"))
        self.icons_item_dir = self.replace_path(os.path.join(base_dir, "icons/icon_item"))
        nuke.pluginAddPath(self.icons_menu_dir)
        nuke.pluginAddPath(self.icons_toolbar_dir)
        nuke.pluginAddPath(self.icons_item_dir)

    def create_menu(self, name, icon_name):
        """
        create nuke menu
        :param name:
        :param icon:
        :return:
        """
        tool_bar = nuke.menu('Nodes')
        menu = tool_bar.addMenu(name, icon=icon_name)
        return menu

    def create_tools(self, menu, type, name, command, shortcut, icon_name):
        """
        create menu tools
        :param type:
        :param menu:
        :param name:
        :param command:
        :param shortcut:
        :param icon:
        :return:
        """
        if type == "python":
            menu.addCommand(name, command, shortcut, icon=icon_name)
        elif type == "gizmo":
            menu.addCommand(name, "nuke.createNode(\"%s\")" % command, icon=icon_name)
        elif type == "toolbar":
            menu.addCommand(name, icon=icon_name)

    def add_bar_tools(self):
        """
        add nuke menu tools
        :return:
        """
        toolbar_config = self.config["toolbar"]
        for menus in toolbar_config:
            # first create tool menu
            menu_icon_name = toolbar_config[menus]['icon']
            cmenu = self.create_menu(menus, menu_icon_name)
            list = toolbar_config[menus]['list']
            for tools in list:
                # second add menu list
                if tools["icon"]:
                    tools_icon = tools["icon"]
                else:
                    tools_icon = ""

                if "max_version" in tools.keys():
                    max_version = tools["max_version"]
                else:
                    max_version = None

                if max_version is None or (self.nuke_version_number <= int(tools["max_version"])):
                    self.create_tools(cmenu,
                                      tools["type"],
                                      tools["name"],
                                      tools["command"],
                                      tools["shortcut"],
                                      tools_icon
                                      )

    def create_menu_tools(self, toolMenu, name, command):
        """
        create_menu_tools
        :param toolMenu:
        :param name:
        :param command:
        :return:
        """
        toolMenu.addCommand(name, command)

    def add_menu_tools(self):
        """
        add_menu_tools
        :return:
        """
        menubar = nuke.menu("Nuke")
        toolMenu = menubar.addMenu('&Tools')
        toolMenu_config = self.config["toolMenu"]
        for tools in toolMenu_config:
            if "max_version" in toolMenu_config[tools].keys():
                max_version = toolMenu_config[tools]["max_version"]
            else:
                max_version = None
            if max_version is None or (self.nuke_version_number <= int(toolMenu_config[tools]["max_version"])):
                self.create_menu_tools(toolMenu,
                                       toolMenu_config[tools]["name"],
                                       toolMenu_config[tools]["command"]
                                       )

    def add_other_tools(self):
        """
        加载第三方完整工具包
        """
        others_config = self.config["others"]
        for item in others_config:
            nuke.pluginAddPath(self.replace_path(os.path.join(self.root_base_dir, others_config[item]["path"])))

    def replace_path(self, path):
        """
        replace path
        :param path:
        :return:
        """
        final_path = path.replace('\\', '/')
        return final_path

    def default_init(self):
        """
        default init
        :return:
        """
        if self.nuke_version_number < 13:
            command.cryptomatte_utilities.setup_cryptomatte()

    def knob_show_frame(self):
        """
        show frame range on knob
        :return:
        """
        nuke.knobDefault("Read.label",
                         "<font size=\"3\" color =#548DD4><b> Frame range :</b></font> "
                         "<font color = red>[value first] - [value last] </font>")

    def knob_after_render(self):
        """
        after write render
        :return:
        """
        nuke.knobDefault("Write.afterRender", "command.run_readFromWrite()")


if __name__ == '__main__':
    run = NukeMenu()
    run.add_bar_tools()
    run.add_menu_tools()
    run.add_other_tools()
    run.knob_show_frame()
    run.knob_after_render()

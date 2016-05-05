# coding=utf-8
# author=weijer
# http://www.cgspread.com
import nuke
from python.packproject import nuke2pack
import python.pw_multiScriptEditor as ScriptEditor
from python.Channel import autoComper, PreCompForArnold, RenderLayer
import python.ToolSet as ToolSet


def run_pack():
    """
    run package nuke project plugin
    :return:
    """
    wgt = nuke2pack.PackageDialog()
    wgt.exec_()


def run_ScriptEditor():
    """
    run script editor
    :return:
    """
    ScriptEditor.showNuke()


def run_autoComper():
    """
    run autoComper script
    :return:
    """
    autoComper.autoComper()


def run_preCompForArnold():
    """
    run preCompForArnold script
    :return:
    """
    PreCompForArnold.preCompForArnold()


def run_RenderLayer():
    """
    run RenderLayer script
    :return:
    """
    RenderLayer.RenderLayer()


def run_presetBackdrop():
    """
    run presetBackdrop script
    :return:
    """
    ToolSet.presetBackdrop.presetBackdrop()


def run_browseDir():
    """
    run browseDir script
    :return:
    """
    ToolSet.browseDir.browseDirByNode()


def run_SingleToEquence():
    """
    run SingleToEquence script
    :return:
    """
    ToolSet.single_to_sequence.main()


def run_switchShot():
    """
    run switch_shot script
    :return:
    """
    ToolSet.switch_shot.main()


def run_correctErrorReadNode():
    """
    run correct_error_read_node script
    :return:
    """
    ToolSet.correct_error_read_node.main()


def run_ListShuffle():
    """
    run correct_error_read_node script
    :return:
    """
    ToolSet.ListShuffle.main()


def run_replaceReadNodePath():
    """
    run replace_read_node_path script
    :return:
    """
    ToolSet.replace_read_node_path.main()


def run_toggleInput():
    """
    run toggle_input script
    :return:
    """
    ToolSet.toggle_input.main()


def run_toggleStamp():
    """
    run toggle_stamp script
    :return:
    """
    ToolSet.toggle_stamp.main()


def run_releaseNotes():
    nuke.message('<p style="color:#99CCFF;font-weight:600">Nuke ToolSet Ver1.0</p>'
                 '<p  style="color:#6699cc;font-weight:600">By weijer</p>'
                 '<p  style="color:#99CCFF;font-weight:600">联系QQ：250557277</p>')

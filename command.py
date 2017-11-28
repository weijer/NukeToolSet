# coding=utf-8
# author=weijer
# http://www.cgspread.com
import os.path

import nuke

import python.CreatePointCloud.CreatedPointCloud as CreatedPointCloud
import python.NukeFXSExporter.NukeFXSExporter as NukeFXSExporter
import python.ToolSet as ToolSet
import python.pw_multiScriptEditor as ScriptEditor
from python.Channel import autoComper, PreCompForArnold, RenderLayer
from python.ToolSet import ReadAfterRender
from python.cryptomatte import cryptomatte_utilities
from python.mamoworld.mochaImportPlus import loadMochaImport
from python.mamoworld.workflow import relativeFilePath
from python.packproject import nuke2pack

base_dir = os.path.dirname(__file__)
loadMochaImport.load()
loadMochaImport.addIconPath(base_dir)

import mochaimport


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


def run_cryptomatte_create():
    """
    run cryptomatte script
    :return:
    """
    cryptomatte_utilities.cryptomatte_create_gizmo()


def run_decryptomatte_all():
    """
    run cryptomatte script
    :return:
    """
    cryptomatte_utilities.decryptomatte_all()


def run_decryptomatte_selected():
    """
    run cryptomatte script
    :return:
    """
    cryptomatte_utilities.decryptomatte_selected()


def run_encryptomatte():
    """
    run cryptomatte script
    :return:
    """
    cryptomatte_utilities.encryptomatte_create_gizmo()


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


def run_relativeFilePath():
    """
    run mamoworld script
    @return:
    """
    relativeFilePath.showReplaceFilePathDialog()


def run_createStabilizedView():
    """
    @return:
    """
    mochaimport.createStabilizedView()


def run_createCornerPin():
    """
    @return:
    """
    mochaimport.createCornerPin()


def run_createTracker4Node():
    """
    @return:
    """
    mochaimport.createTracker4Node()


def run_createTracker3Node():
    """
    @return:
    """
    mochaimport.createTracker3Node()


def run_createRotoPaintNodeMI():
    """
    @return:
    """
    mochaimport.createRotoPaintNodeMI()


def run_createRotoNodeMI():
    """
    @return:
    """
    mochaimport.createRotoNodeMI()


def run_createGridWarpNodeMI():
    """
    @return:
    """
    mochaimport.createGridWarpNodeMI()


def run_createTransformNodeMI():
    """
    @return:
    """
    mochaimport.createTransformNodeMI()


def run_createCameraAndPointCloud():
    """
    @return:
    """
    mochaimport.createCameraAndPointCloud()


def run_createCameraRig():
    """
    @return:
    """
    mochaimport.createCameraRig()


def run_showSettings():
    """
    @return:
    """
    mochaimport.showSettings()


def run_createdPointCloud():
    """
    @return:
    """
    CreatedPointCloud.create_cloud_point()


def run_nukeFXSExporter():
    """
    @return:
    """
    NukeFXSExporter.silhouetteFxsExporter()


def run_readFromWrite():
    """
    @return:
    """
    ReadAfterRender.RenderWrite().read_from_write()


def run_releaseNotes():
    nuke.message('<p style="color:#99CCFF;font-weight:600">Nuke ToolSet Ver1.0</p>'
                 '<p  style="color:#6699cc;font-weight:600">By weijer</p>'
                 '<p  style="color:#99CCFF;font-weight:600">联系QQ：250557277</p>')

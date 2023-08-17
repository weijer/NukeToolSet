import  os
import shutil

import nuke




file_path=os.path.dirname(__file__).replace('\\', '/')
nuke.pluginAddPath("python/mamoworld2/mochaImportPlus/mochaimport")
def addIconPath(base_dir):
    """
    @param base_dir:
    @return:
    """
    icons_mocha_dir = replace_path(os.path.join(base_dir, "python/mamoworld2/mochaImportPlus/icons"))
    nuke.pluginAddPath(icons_mocha_dir)

def replace_path(path):
    """
    replace path
    :param path:
    :return:
    """
    final_path = path.replace('\\', '/')
    return final_path

def remove_old(file):
    if os.path.isfile(file_path+"/"+file):
        os.remove(file_path+"/"+file)
    elif os.path.isdir(file_path+"/"+file):
        shutil.rmtree(file_path+"/"+file)



old_list=["version_03f30d0a","version_420d0d0a","version_610d0d0a","version_d1f20d0a","CornerPinMI.gizmo","EndStabilized.gizmo","StartStabilized.gizmo"]
for i in old_list:
    remove_old(i)

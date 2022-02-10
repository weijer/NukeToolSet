#coding:utf-8
import nuke,os

#插件路径的不确定性，没法使用固定路径，只能全部添加


dir_list = ["gizmos", "Channel"]#要添加的文件夹,暂时只知道这2个里面有gizmo节点，需要添加的pluginpath里，其他的路径还为发现错误

for nukepath in nuke.pluginPath():
    for dir in dir_list:
        file_path = "{}/{}".format(nukepath, dir)
        if os.path.isdir(file_path):
            for root,dirs,files in os.walk(file_path):
                for dir in dirs:
                    dirpath = "{}/{}".format(file_path, dir)
                    if not dirpath in nuke.pluginPath():
                        nuke.pluginAddPath(dirpath)

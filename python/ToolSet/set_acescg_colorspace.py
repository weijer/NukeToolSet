import nuke


def main():
    nuke.root()["colorManagement"].setValue("OCIO")  # 启用OCIO模式
    nuke.root()["OCIO_config"].setValue(3)  # 3表示使用自定义路径
    nuke.root()["customOCIOConfigPath"].setValue("E:/nodejs/jspython/py_scripts/config/aces_1_3/config.ocio")  # 设置路径

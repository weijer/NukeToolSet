import nuke


def main():
    nuke.root()["colorManagement"].setValue("OCIO")  # 启用OCIO模式
    nuke.root()["OCIO_config"].setValue(3)  # 3表示使用自定义路径
    nuke.root()["customOCIOConfigPath"].setValue("C:/Teamones/dcc/rez_package/ocio/aces_1.3/config.ocio")  # 设置路径

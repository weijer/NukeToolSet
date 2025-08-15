import nuke


def main():
    nuke.root()["colorManagement"].setValue("Nuke")  # 启用Nuke默认模式
    nuke.root()["OCIO_config"].setValue(2)  # 1表示使用自定义路径
    nuke.root()["customOCIOConfigPath"].setValue("")  # 设置路径

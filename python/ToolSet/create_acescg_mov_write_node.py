import nuke


def main():
    write_node = nuke.createNode("Write")
    write_node.setName("TeonesWrite")
    write_node["channels"].setValue("rgb")
    write_node["colorspace"].setValue("color_picking")
    write_node["file_type"].setValue("mov")
    write_node["mov_prores_codec_profile"].setValue("ProRes 4:4:4:4 12-bit")
    write_node["create_directories"].setValue(True)

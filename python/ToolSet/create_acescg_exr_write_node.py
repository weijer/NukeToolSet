import nuke


def main():
    write_node = nuke.createNode("Write")
    write_node.setName("TeonesWrite")
    write_node["channels"].setValue("rgb")
    write_node["colorspace"].setValue("compositing_linear")
    write_node["file_type"].setValue("exr")
    write_node["datatype"].setValue("32 bit float")
    write_node["compression"].setValue("PIZ Wavelet (32 scanlines)")
    write_node["create_directories"].setValue(True)

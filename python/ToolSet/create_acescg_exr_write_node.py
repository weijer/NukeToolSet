import nuke


def main():
    write_node = nuke.createNode("Write")
    write_node.setName("TeonesWrite")
    write_node["channels"].setValue("rgb")
    write_node["colorspace"].setValue("compositing_linear")
    write_node["file_type"].setValue("exr")
    write_node["datatype"].setValue("16 bit half")
    write_node["compression"].setValue("Zip (1 scanline)")
    write_node["create_directories"].setValue(True)

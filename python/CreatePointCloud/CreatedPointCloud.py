# coding=utf8
import nuke
import random

MAX_POINTS_COUNTS = 300000


def create_cloud_point():
    file_path, max_points = select_plyfile_dialog()
    if not file_path:
        return
    node_name = file_path.split("/")[-1]
    read_data = scan_ply_data(file_path, max_points)
    create_node(node_name, read_data)


def select_plyfile_dialog():
    p = nuke.Panel(".ply importer")
    p.addFilenameSearch(".ply file", "")
    p.addSingleLineInput("Maximum points to create", MAX_POINTS_COUNTS)
    p.addButton("Cancel")
    p.addButton("OK")
    p.show()
    path = p.value(".ply file") or None
    if path:
        max_points = int(p.value("Maximum points to create"))
        return path, max_points
    return None, None

def scan_ply_data(path, max_points):
    started = False
    total = 0
    points = ""
    normals = ""
    colors = ""
    vert_entries = []
    verts_count = 0
    with open(path) as r:
        lines = r.readlines()
    for line in lines:
        if "element vertex" in line:
            verts_count = int(line.split()[2])
            print "%s points detected! " % verts_count
        if started and total < verts_count:
            vert_entries.append(line)
            total += 1
        if "end_header" in line:
            started = True
    if max_points <= verts_count:
        print "selecting only %s points at random! " % max_points
        vert_entries = randomSelection(max_points, vert_entries)
    for entry in vert_entries:
        data_split = entry.split()
        points += "%s " % " ".join(data_split[0:3])
        normals += "%s " % " ".join(data_split[3:6])
        colors += "%s " % " ".join([str(float(v) / 255.0) for v in data_split[6:9]])  # ignore alpha value
    read_data = {"total": total, "points": points, "normals": normals, "colors": colors, "verts_count": verts_count}
    return read_data


def randomSelection(numToPick, items):
    shuffledItems = items
    random.shuffle(shuffledItems)
    return shuffledItems[0:numToPick]


def create_node(node_name, read_data):
    label = "%s points" % (read_data["verts_count"])
    node = nuke.createNode("BakedPointCloud")
    node.knob("serializePoints").setValue("%s %s" % (read_data["total"], read_data["points"]))
    node.knob("serializeNormals").setValue("%s %s" % (read_data["total"], read_data["normals"]))
    node.knob("serializeColors").setValue("%s %s" % (read_data["total"], read_data["colors"]))
    node.knob("name").setValue(node_name)
    node.knob("label").setValue(label)


if __name__ == "__main__":
    create_cloud_point()

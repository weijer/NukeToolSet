import nuke
import bakeGizmos


def bakeCornerPinMI(gizmo):
    return bakeAnyGizmo(gizmo)


def bakeStabilizedViewStart(startGizmo):
    return bakeAnyGizmo(startGizmo)


def bakeStabilizedViewEnd(endGizmo):
    return bakeAnyGizmo(endGizmo)


def bakeAnyGizmo(gizmo):
    for each in nuke.allNodes():
        each.knob("selected").setValue(False)

    nodeName = gizmo.knob('name').value()
    nodeTileColor = gizmo.knob('tile_color').value()

    group = bakeGizmos.bakeGizmo(gizmo)

    group.knob('name').setValue(nodeName)
    group.knob('tile_color').setValue(nodeTileColor)

    return group

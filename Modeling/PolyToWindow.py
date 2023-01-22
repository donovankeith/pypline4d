"""Name-en-US: Polys to Window
Description-en-US: Converts the currently selected polygon objects to windows
"""

import c4d
from c4d import gui
# Welcome to the world of Python


def main():
    c4d.CallCommand(12187)  # Polygons
    c4d.CallCommand(12112)  # Select All
    c4d.CallCommand(450000004)  # Extrude Inner
    tool()[c4d.MDATA_EXTRUDEINNER_PRESERVEGROUPS] = True
    tool()[c4d.MDATA_EXTRUDEINNER_OFFSET] = 1
    c4d.CallCommand(450000004)  # Extrude Inner
    tool()[c4d.MDATA_EXTRUDEINNER_PRESERVEGROUPS] = False
    tool()[c4d.MDATA_EXTRUDEINNER_OFFSET] = 1
    c4d.CallCommand(12109)  # Delete
    c4d.CallCommand(12112)  # Select All
    c4d.CallCommand(1011183)  # Extrude
    tool()[c4d.MDATA_EXTRUDE_CREATECAPS] = True
    tool()[c4d.MDATA_EXTRUDE_OFFSET] = -2
    c4d.CallCommand(12112)  # Select All
    c4d.CallCommand(14041)  # Reverse Normals
    c4d.CallCommand(450000003)  # Smooth Shift
    tool()[c4d.MDATA_SMOOTHSHIFT_OFFSET] = 0.1


if __name__ == '__main__':
    main()

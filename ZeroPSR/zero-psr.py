"""
Zero PSR
Sets Position/Rotation of active objects to (0, 0, 0) and Scale to (1, 1, 1).

by
Donovan Keith

CHANGELOG:
v0.1: Updated active object loop to be R13 compatible.
v0.0: Main functionality implemented

TO DO:
* Add an undo buffer
"""

import c4d
from c4d import gui
# Welcome to the world of Python


def main():
    # Get the active objects
    objs = doc.GetActiveObjects(flags=c4d.GETACTIVEOBJECTFLAGS_0)

    # Loop through the active objects
    for obj in objs:
        # Set Position and Rotation to 0, 0, 0
        obj.SetRelPos(c4d.Vector(0.0))
        obj.SetRelRot(c4d.Vector(0.0))

        # Set Scale to 1, 1, 1
        obj.SetRelScale(c4d.Vector(1.0))

    c4d.EventAdd()


if __name__ == '__main__':
    main()

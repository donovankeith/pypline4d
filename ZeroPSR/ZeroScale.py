"""
Zero Scale
Despite the name, this sets Scale of active objects to (1, 1, 1). Think of "zero" as "reset".

by
Donovan Keith

TO DO:
Rename to have it make more sense.
"""

import c4d
from c4d import gui


def main():
    # Get the active objects
    objs = doc.GetActiveObjects(flags=c4d.GETACTIVEOBJECTFLAGS_0)

    # Loop through the active objects
    for obj in objs:
        # Set Scale to 1, 1, 1
        obj.SetRelScale(c4d.Vector(1.0))

    c4d.EventAdd()


if __name__ == '__main__':
    main()

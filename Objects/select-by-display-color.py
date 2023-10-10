"""Name-en-US: DK-Select Objects By Display Color
Description-en-US: Selects Objects with a Similar Display Color

This script is most useful for flat hierarchies of objects imported from
CAD programs. It's not recommened for scenes with complex hierarchies or
those with existing animations.

## Usage Instructions

1. Select the objects whose colors you want to match.
2. Run this Script.

## Thanks

Written in response to [this request](https://forums.cgsociety.org/t/select-objects-by-display-color/2050047/5)
from LonChaney on CG Talk.

## License

The MIT License (MIT)

Copyright (c) 2019 Donovan Keith <donovanskeith@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Imports
# =======

import c4d
from c4d import gui

# Menu State
# ==========


def state():
    """Command is available if any object is selected.
    """

    if op or doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0):
        return True
    else:
        return False

# Utility Functions
# =================


def GetNextObject(op):
    """Retrieve the next object in the document.
    Source: https://developers.maxon.net/?p=596
    """

    if op == None:
        return None

    if op.GetDown():
        return op.GetDown()

    while not op.GetNext() and op.GetUp():
        op = op.GetUp()

    return op.GetNext()

# Main Logic
# ==========


def main():
    active_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    colors = []

    # Store a list of all selected colors
    for obj in active_objects:
        color = c4d.Vector(op[c4d.ID_BASEOBJECT_COLOR])
        if color not in colors:
            colors.append(color)

    doc.StartUndo()

    # Select objects that match the color
    obj = doc.GetFirstObject()
    while obj:
        if not obj.GetBit(c4d.BIT_ACTIVE):
            color = c4d.Vector(obj[c4d.ID_BASEOBJECT_COLOR])
            if color in colors:
                doc.SetActiveObject(obj, c4d.SELECTION_ADD)

        obj = GetNextObject(obj)

    doc.EndUndo()
    c4d.EventAdd()


# Execute main()
if __name__ == '__main__':
    main()

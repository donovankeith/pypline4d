"""Name-en-US: DK-Aim At
Description-en-US: Select all objects you want to aim, then select the target before running this command.

## Usage Instructions

1. Select the the objects you want to aim.
2. Hold down Ctrl and select the object you want to Aim At.
3. Run this Script.

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

import c4d
from c4d import gui


def state():
    """Only show as active if 2+ objects are selected."""
    active_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if active_objects and len(active_objects) >= 2:
        return True
    return False

# Main function


def main():
    active_objects = doc.GetActiveObjects(
        c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if not active_objects:
        return

    # Retrieve the target's global position
    target = active_objects.pop()
    target_mg = target.GetMg()
    target_pos = target_mg.off

    doc.StartUndo()
    for obj in active_objects:
        if not obj:
            continue

        # Store object's starting global matrix and position for calculations
        obj_mg = obj.GetMg()
        obj_pos = obj_mg.off

        # Calculate direction to target
        obj_to_target = (target_pos - obj_pos).GetNormalized()
        up_vector = c4d.Vector(0.0, 1.0, 0.0)  # Try to point the Y-Axis up

        # Build a global matrix to orient towards the object
        aim_mg = c4d.Matrix()
        aim_mg.v3 = obj_to_target  # Point Z-Axis at target
        aim_mg.v2 = up_vector  # Force Y-Axis to point up at world Y
        # X-Axis is perpindicular to plane formed by Z and Y
        aim_mg.v1 = up_vector.Cross(obj_to_target).GetNormalized()
        # Recalculate Y-Axis to be actually perpindicular to X and Z.
        aim_mg.v2 = obj_to_target.Cross(aim_mg.v1).GetNormalized()

        # Move and Scale matrix to match how object started
        aim_mg.off = obj_mg.off
        aim_mg.v1 *= obj_mg.v1.GetLength()
        aim_mg.v2 *= obj_mg.v2.GetLength()
        aim_mg.v3 *= obj_mg.v3.GetLength()

        # Rotate object to point at target
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetMg(aim_mg)

    doc.EndUndo()
    c4d.EventAdd()


# Execute main()
if __name__ == '__main__':
    main()

"""Name-en-US: DK-Group Objects By Display Color
Description-en-US: Groups all objects in scene by display color. WARNING: Breaks existing parent/child relationships and deformer/generator setups.

## Usage Instructions

1. Save a backup of your scene.
2. Run this script.

## Known Issues

Not really working at the moment.

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

# Main function


def main():
    colors_objects_mgs = {}

    doc.StartUndo()

    c4d.StatusSetText("[1/2]: Collating by color.")
    c4d.StatusSetSpin()

    # Store objects by color
    obj = doc.GetFirstObject()
    while obj:
        color = obj[c4d.ID_BASEOBJECT_COLOR]
        color_string = repr(color)
        mg = obj.GetMg()

        obj_mg = (obj, mg)

        if color_string in colors_objects_mgs.keys():
            colors_objects_mgs[color_string].append(obj_mg)
        else:
            colors_objects_mgs[color_string] = [obj_mg]

        obj = GetNextObject(obj)

    c4d.StatusSetText("[2/2]: Grouping Objects.")
    # Build groups of objects by color
    pred_null = None
    for color_string, obj_mg_list in colors_objects_mgs.items():
        # Find the center position of the objects
        average_pos = c4d.Vector(0.0)

        for obj, mg in obj_mg_list:
            average_pos += mg.off

        average_pos /= float(len(obj_mg_list))

        # Create a null centered between the objects
        null_obj = c4d.BaseObject(c4d.Onull)

        # Make it the same color as the objects
        null_obj[c4d.ID_BASEOBJECT_USECOLOR] = 1  # Automatic Mode
        print(color_string)
        null_obj[c4d.ID_BASEOBJECT_COLOR] = eval("c4d." + color_string)
        null_obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2  # Display color

        # Center the null
        center_mg = c4d.Matrix()
        mg.off = average_pos

        # Ensure nulls are inserted roughly in the same order colors first occurred in the scene.
        doc.InsertObject(null_obj, pred=pred_null)
        pred_null = null_obj

        # Center the null
        null_obj.SetMg(center_mg)
        doc.AddUndo(c4d.UNDOTYPE_NEW, null_obj)

        # Move objects of the came color under the new null
        pred = None
        for obj, mg in obj_mg_list:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            obj.Remove()
            doc.InsertObject(obj, parent=null_obj, pred=pred)
            obj.SetMg(mg)
            pred = obj

    doc.EndUndo()
    c4d.EventAdd()
    c4d.StatusClear()


# Execute main()
if __name__ == '__main__':
    main()

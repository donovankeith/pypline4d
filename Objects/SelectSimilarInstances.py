"""Name-en-US: DK-Select Similar Instances
Description-en-US: Selects all Instances of the Selected Object(s)

## Usage Instructions

1. Select an instance or an object referenced by instances
2. Run this Script.
3. All similar instances will be selected.

## Known Limitations

* Instances of Instances will not be selected (this is to allow you to select on any instance
and select any similar instance)    

## Thanks

Written in response to a request by Thomas Phieler.

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


def GetNextObject(op):
    if op == None:
        return None

    if op.GetDown():
        return op.GetDown()

    while not op.GetNext() and op.GetUp():
        op = op.GetUp()

    return op.GetNext()


def IterateHierarchy(op):
    if op is None:
        return

    count = 0

    while op:
        count += 1
        op = GetNextObject(op)

    return count


def main():
    active_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not active_objects:
        return

    doc.StartUndo()

    # Make a list of selected instance "masters"
    masters = []
    for obj in active_objects:
        if obj.GetType() == c4d.Oinstance:
            ref = obj[c4d.INSTANCEOBJECT_LINK]
            if ref is not None:
                masters.append(ref)
        else:
            masters.append(ref)

    # Select all instances of "masters"
    obj = doc.GetFirstObject()
    while obj:
        if obj.GetType() == c4d.Oinstance:
            ref = obj[c4d.INSTANCEOBJECT_LINK]
            if (ref is not None) and (ref in masters):
                doc.SetActiveObject(obj, c4d.SELECTION_ADD)
        elif obj in masters:
            doc.SetActiveObject(obj, c4d.SELECTION_ADD)

        obj = GetNextObject(obj)

    doc.EndUndo()
    c4d.EventAdd()


# Execute main()
if __name__ == '__main__':
    main()

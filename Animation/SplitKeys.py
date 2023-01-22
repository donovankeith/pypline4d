"""
Split Keys
Takes the selected keys and splits them into two keys.
Written for CINEMA 4D R14.025

LICENSE:
Copyright (C) 2012 by Donovan Keith (www.donovankeith.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE

INSTRUCTIONS:

KNOWN LIMITATIONS:

TO DO:
Get their current times
Delete them
Add undo support using doc.AddUndo()
Add support for the currently active timeline
Add support for f-curve selection
Add support for collisions with nearby keyframes

CHANGELOG:
v0.01: 
-

Name-US: Moving Hold
Description-US: Split selected keys at current time
"""

import c4d

debug = True


def GetNextObject(obj, stop_at):
    """
    Walks the hierarchy, stops at "stop_at"
    """
    if obj == None:
        return None

    if obj.GetDown():
        return obj.GetDown()

    while not obj.GetNext() and obj.GetUp() and obj.GetUp() != stop_at:
        obj = obj.GetUp()

    return obj.GetNext()


def GetAllObjects():
    """
    Returns a list of all objects in the document
    """
    first_obj = doc.GetFirstObject()
    obj = doc.GetFirstObject()
    objects = []

    while obj is not None:
        objects.append(obj)
        obj = GetNextObject(obj, first_obj)

    return objects


def GetKeys(track):
    """
    Returns all of track's keys.
    """
    keys = []

    if track == None:
        return keys

    # Get all of the keys
    curve = track.GetCurve()
    key_count = curve.GetKeyCount()

    for i in xrange(key_count):
        keys.append(curve.GetKey(i))

    return keys


def KeyIsSelected(key):
    """
    Returns true if the key is selected, false otherwise.
    """

    # Timeline selection bits
    tl1 = key.GetNBit(c4d.NBIT_TL1_SELECT)
    tl2 = key.GetNBit(c4d.NBIT_TL2_SELECT)
    tl3 = key.GetNBit(c4d.NBIT_TL3_SELECT)
    tl4 = key.GetNBit(c4d.NBIT_TL4_SELECT)

    # F-Curve selection bits
    fc1 = key.GetNBit(c4d.NBIT_TL1_FCSELECT)
    fc2 = key.GetNBit(c4d.NBIT_TL2_FCSELECT)
    fc3 = key.GetNBit(c4d.NBIT_TL3_FCSELECT)
    fc4 = key.GetNBit(c4d.NBIT_TL4_FCSELECT)

    return tl1 or tl2 or tl3 or tl4 or fc1 or fc2 or fc3 or fc4


def GetSelectedKeys(track):
    """
    Returns all selected keyframes for a given track
    """

    # Find all keys
    keys = GetKeys(track)
    selected_keys = []

    # Loop through all keys
    for key in keys:
        # Is it selected in the timeline?
        if KeyIsSelected(key):
            selected_keys.append(key)

    return selected_keys


def main():
    doc.StartUndo()

    # Loop through all objects
    objs = GetAllObjects()

    for obj in objs:
        # Loop through all tracks
        tracks = obj.GetCTracks()

        for track in tracks:
            # Find all selected keys
            selected_keys = GetSelectedKeys(track)

            # Loop through selected keys:
            if selected_keys == []:
                continue

            if debug == True:
                print(obj.GetName() + ', ' + track.GetName() + ':')
            for key in selected_keys:
                if debug == True:
                    print(key.GetValue())

    doc.EndUndo()


if __name__ == '__main__':
    main()

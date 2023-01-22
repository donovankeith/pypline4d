"""Name-en-US: Compound Boolean Union
Description-en-US: Takes all selected objects, and combines them into a nested boolean hierarchy
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
Select 2+ objects
Run the script

TO DO:
Adjust object selections after the fact so that you can easily delete the originals
Decide if you want a different behavior for dealing with originals (hide them? remove them from their hierarchies and use them?)

CHANGELOG:
v0.01: Added basic functionality.

Name-US: Boolean Union Compound
Description-US: Combine all selected objects into one boolean
"""

import c4d
from c4d import gui
#Welcome to the world of Python

def make_boole_union(obj_a, obj_b):
    """Take obj_a and obj_b and combines them under a boolean union object.
    returns the boolean object. Make sure that these objects aren't attached
    to a scene as this function does not clone them"""

    #If we're missing any objects, return
    if obj_a is None or obj_b is None:
        return
    
    #Create a union type boolean object
    boole = c4d.BaseObject(c4d.Oboole)
    boole[c4d.BOOLEOBJECT_TYPE] = 0 #A Union B

    #Put them inside the boole
    obj_a.InsertUnder(boole)
    obj_b.InsertUnder(boole)
    
    #Rename the boolean object to: ObjA + ObjB
    boole.SetName( obj_a.GetName() + " + " + obj_b.GetName())
    
    #Return the boolean object
    return boole

def main():
    #Get the selected objects
    objs = doc.GetActiveObjects(flags=c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if objs is None or len(objs) <2:
        gui.MessageDialog('You need to select 2+ objects to run this command.')
        return

    #Loop through all the objects, making booles along the way
    prev_boole = make_boole_union(objs[1].GetClone(c4d.COPYFLAGS_NO_HIERARCHY), objs[0].GetClone(c4d.COPYFLAGS_NO_HIERARCHY))

    latter_objs = objs[2:]
    print(latter_objs)

    for obj in latter_objs:
        print("In the latter_objs")
        print(obj.GetName())
        prev_boole = make_boole_union(obj.GetClone(c4d.COPYFLAGS_NO_HIERARCHY), prev_boole.GetClone())

    #Add the objects to the document    
    doc.InsertObject(prev_boole)
    
    #Tell C4D something has changed
    c4d.EventAdd()

if __name__=='__main__':
    main()

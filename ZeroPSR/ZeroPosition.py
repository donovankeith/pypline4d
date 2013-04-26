import c4d
from c4d import gui
#Welcome to the world of Python

"""
Zero Position v0.01
Takes the currently selected objects and sets their position to 0,0,0

by
Donovan Keith

CHANGELOG:
v0.1: Updated active object loop to be R13 compatible.
v0.0: Main functionality implemented
"""

def main():
    #Get the active objects
    objs = doc.GetActiveObjects(flags=c4d.GETACTIVEOBJECTFLAGS_0)

    #Loop through the active objects
    for obj in objs:
        #Set Position
        obj.SetRelPos(c4d.Vector(0.0))

    c4d.EventAdd()

if __name__=='__main__':
    main()
"""Name-en-US: Animate on Spline v0.01
Description-en-US: Creates an Align To Spline tag with keys at the start/end of animation.

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
1. Select the object(s) you want to animate along a spline
2. Continue selecting, select the spline you want to animate onto last.
3. Run the "Animate on Spline" command.

WHAT HAPPENED:
You now have an align to spline tag with keys on the first and last frames
it is pointing to the spline you selected last, or to nothing if
you did not select a spline last.

TO DO:
Add support for auto-assign-to-spline even if spline
isn't the last object in a list of objects.

CHANGELOG:
v0.01: Created basic functionality.
-

Name-US: Animate on Spline
Description-US: Takes the selected objects, and adds an Align To Spline tag with keyframes.
"""

import c4d

def main():
    doc.StartUndo()

    #Loop through all active objects
    #Get the active objects in order
    objs = doc.GetActiveObjects(flags=c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    #If there aren't any objects, return
    if len(objs) == 0:
        return
    
    #The spline is the last object in the list.
    spline = None
    
    #If there's more than one object selected, the last can be
    #a spline
    if len(objs) > 1:    
        #Test to see if it's a spline
        if objs[-1].GetRealSpline():
            #If it is, amend the object list
            spline = objs.pop()
            
        #If the user only selected two objects, don't worry about order.
        elif (len(objs) == 2) and objs[0].GetRealSpline:
            objs.reverse()
            spline = objs.pop()
        
        #If you've found a spline...
        if spline is not None:    
            #Adjust interpolation to Uniform
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, spline)
            spline[c4d.SPLINEOBJECT_INTERPOLATION] = 2

    #Preload Start/End Times
    start_time = doc.GetMinTime()
    end_time = doc.GetMaxTime()

    #Keep track of whether any tags are already selected
    selected = False

    #For every selected object
    for obj in objs:
        #Add an Align to Spline Tag
        tag = c4d.BaseTag(c4d.Taligntospline)
        if spline is not None:
            tag[c4d.ALIGNTOSPLINETAG_LINK] = spline
        obj.InsertTag(tag)
        
        #Create a track
        track = c4d.CTrack(tag, c4d.DescID(c4d.DescLevel(c4d.ALIGNTOSPLINETAG_POSITION, c4d.DTYPE_REAL, 0)))
        tag.InsertTrackSorted(track)
        curve = track.GetCurve()
        
        #Create a Key at frame 0
        start_key = c4d.CKey()
        start_key.SetTime(curve, start_time)
        start_key.SetValue(curve,0.0)
        curve.InsertKey(start_key)
        
        #Create a Key at last frame
        end_key = c4d.CKey()
        end_key.SetTime(curve, end_time)
        end_key.SetValue(curve, 1.0)
        curve.InsertKey(end_key)
        
        #Set default key interpolation.
        curve.SetKeyDefault(doc,0) #Key 0: Start Key
        curve.SetKeyDefault(doc,1) #Key 1: End Key
        
        #Select the new tags
        if not selected:
            doc.SetActiveTag(tag, c4d.SELECTION_NEW)
            selected = True
        else:
            doc.SetActiveTag(tag, c4d.SELECTION_ADD)
        
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
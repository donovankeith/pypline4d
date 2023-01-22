"""Name-en-US: Camera Morph Keys
Description-en-US: Takes first selected CameraMorph tag and automatically add keys based on the
number of objects in the multi-morph list.

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
Select a camera morph tag.
Run this script.

TO DO:
Multi-select support.
Improve behavior if there are pre-existing keys.

CHANGELOG:
v0.01: Added basic functionality.
v0.02: Added undo, and corrected key spacing. Auto-add
        key even when there are < 2 cameras.

Name-US: Camera Morph Keys
Description-US: Creates a keyframe for each camera in the selected camera morph tag.
"""

import c4d

def main():
    doc.StartUndo()

    #Get the CameraMorph tag
    tag = doc.GetActiveTag()
    
    #Stop if the tag is of the wrong type
    if tag is None or tag[c4d.TMORPHCAM_LIST_LINKS] is None:
        return

    cam_list_raw = tag[c4d.TMORPHCAM_LIST_LINKS]
    cam_count = cam_list_raw.GetObjectCount()

    #Find the blend track
    blend_track = tag.FindCTrack(c4d.TMORPHCAM_BLEND)
    
    #If there isn't a blend track, create and insert it.
    if blend_track is None:
        blend_track = c4d.CTrack(tag, c4d.DescID(c4d.DescLevel(c4d.TMORPHCAM_BLEND, c4d.DTYPE_REAL, 0)))
        tag.InsertTrackSorted(blend_track)

    #Get the track's F-Curve, and delete existing keys
    curve = blend_track.GetCurve()
    curve.FlushKeys()
    
    #If there are 1 or fewer cameras, pretend there are two
    if cam_count==0 or cam_count==1:
        cam_count = 2 #So that we can have a key at 0 and 100%
    
    #Get document timing info
    min_time = doc.GetMinTime().Get()
    max_time = doc.GetMaxTime().Get()
    length_time = max_time - min_time
    time_chunk = length_time/(cam_count-1)
    fps = doc.GetFps()
    
    #Add a key for each camera
    #doc.AddUndo(c4d.UNDOTYPE_CHANGE,op)
    for i in range(cam_count):
        #Create a key
        key = c4d.CKey()
        
        #Evenly distribute value
        value = 0.0
        if i is not 0:
            value = (1.0 / float(cam_count-1)) * float(i)
        key.SetValue(curve, value)
        
        #Calculate the correct time
        ideal_time = c4d.BaseTime(time_chunk*i + min_time)
        ideal_time.Quantize(fps)
        
        #Set the key time
        key.SetTime(curve, ideal_time)
        curve.InsertKey(key)
        doc.AddUndo(c4d.UNDOTYPE_NEW, key)
        
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
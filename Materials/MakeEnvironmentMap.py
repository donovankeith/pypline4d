"""
Make Environment Map v0.01
Renders an environment map for the selected object.
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
Add undo support using doc.AddUndo()
Add support to save images automatically
Add support to automatically replace reflection channel
 of material with environment channel (include reflection maps, et)


CHANGELOG:
v0.01: 
-

Name-US: MakeEnvironmentMap
Description-US: Takes the selected object and generates an environment map.
"""

import c4d

def main():
    doc.StartUndo()

    #Loop through all active objects
    obj = doc.GetActiveObject()
    if obj is None: return

    #Create 100% reflective material
    silver_mat = c4d.BaseMaterial(type=c4d.Mmaterial)
    silver_mat[c4d.MATERIAL_USE_COLOR] = False
    silver_mat[c4d.MATERIAL_USE_REFLECTION] = True
    silver_mat[c4d.MATERIAL_USE_SPECULAR] = False
    silver_mat.SetName("100% Reflective")
    doc.InsertMaterial(silver_mat)

    #Get the object's PSR
    obj_mg = obj.GetMg()
    
    #Temporarily hide it.
    start_render_mode = obj.GetRenderMode()
    obj.SetRenderMode(c4d.MODE_OFF)
    
    #Create an environment sphere
    sphere = c4d.BaseObject(c4d.Osphere)
    sphere.SetName(obj.GetName() + " Env Probe")
    sphere.SetMg(obj_mg) #Move to OBJ
    sphere[c4d.PRIM_SPHERE_RAD] = 1.0 #Give small radius

    #Give the sphere a wholly reflective material
    tex_tag = c4d.TextureTag()
    tex_tag.SetMaterial(silver_mat)
    tex_tag[c4d.TEXTURETAG_PROJECTION] = 0 #Spherical projection
    
    #Insert the tag
    sphere.InsertTag(tex_tag)
    
    #Add a bake texture tag
    bake_tag = c4d.BaseTag(c4d.Tbaketexture)
    
    #Set bake texture values for environment map
    bake_tag[c4d.BAKETEXTURE_WIDTH] = 1000
    bake_tag[c4d.BAKETEXTURE_HEIGHT] = 500
    bake_tag[c4d.BAKETEXTURE_SUPERSAMPLING] = 1
    bake_tag[c4d.BAKETEXTURE_CHANNEL_REFLECTION] = True #Bake reflection

    #Add filename
    tex_path = obj.GetName()
    bake_tag[c4d.BAKETEXTURE_NAME] = obj.GetName()

    #Add bake tag to sphere
    sphere.InsertTag(bake_tag)

    #Insert the sphere
    doc.InsertObject(sphere)
    
    #Bake the object - tex name is ObjName_ENV
    c4d.CallButton(bake_tag,c4d.BAKETEXTURE_BAKE)

    #Delete the sphere
    #sphere.Remove()
    
    #Restore visibility
    obj.SetRenderMode(start_render_mode)

    #Delete the material
    #silver_mat.Remove()

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
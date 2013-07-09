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

    #Open a save dialog
    doc_path = doc[c4d.DOCUMENT_PATH]
    default_name = '' + obj.GetName() + "_env"
    img_path = c4d.storage.SaveDialog(c4d.FILESELECTTYPE_IMAGES, title="Bake to...", def_path=doc_path)
    if img_path is None: return

    #Add bake tag to sphere
    sphere.InsertTag(bake_tag)

    #Insert the sphere
    doc.InsertObject(sphere)
    
    #Add filename
    bc = bake_tag.GetData()
    bc.SetFilename(c4d.BAKETEXTURE_NAME, img_path)
    bake_tag.SetData(bc)
    
    #Bake the object - tex name is ObjName_ENV
    c4d.CallButton(bake_tag,c4d.BAKETEXTURE_BAKE)

    #Delete the sphere
    #sphere.Remove()
    
    #Restore visibility
    obj.SetRenderMode(start_render_mode)

    #Delete the material
    #silver_mat.Remove()

    #clone the current material
    def GetLastMaterial(obj):
        tags = obj.GetTags()
        cur_tag = None

        #Keep popping until you find a material
        while len(tags)>0 and cur_tag is not None:
            #If it's a texture tag, return its material
            if isinstance(cur_tag, c4d.TextureTag):
                return cur_tag.GetMaterial()
            
            #Not a texture tag, go to the next one
            cur_tag = tags.pop()

        #None of the tags are materials, return None
        return None
    
    #Get the right-most material
    ref_material = GetLastMaterial(obj)
    env_material = None
    
    #If there isn't one, make one
    if ref_material is None:
        env_material = c4d.BaseMaterial(c4d.Mmaterial)
    #If there is, make a clone
    else:
        env_material = ref_material.GetClone()

    #Make a new material
    env_material.SetName(env_material.GetName() + " Env")
    
    if ref_material:
        #Turn on Env if obj is Reflective
        env_material[c4d.MATERIAL_USE_ENVIRONMENT] = ref_material[c4d.MATERIAL_USE_REFLECTION]
        
        #Use the same color
        env_material[c4d.MATERIAL_ENVIRONMENT_COLOR] = ref_material[c4d.MATERIAL_REFLECTION_COLOR]
        
        #Use the same brightness
        env_material[c4d.MATERIAL_ENVIRONMENT_BRIGHTNESS] = ref_material[c4d.MATERIAL_REFLECTION_BRIGHTNESS]
        
        #Set mix mode to multiply
        env_material[c4d.MATERIAL_REFLECTION_TEXTUREMIXING] = 3

    """
    ref_tex = env_material[c4d.MATERIAL_REFLECTION_SHADER].GetClone()
    env_tex = ref_tex.GetClone()
    env_texture[c4d.BITMAPSHADER_FILENAME] = img_path + "Reflection.psd"
    env_material[c4d.MATERIAL_ENVIRONMENT_SHADER]= env_texture
    env_material.InsertShader(env_texture)
    """
    
    doc.InsertMaterial(env_material)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
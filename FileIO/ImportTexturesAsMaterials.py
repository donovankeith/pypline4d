"""Name-en-US: Import Textures as Materials
Description-en-US: Select a directory and load the textures.

WARNING: This is not fully functional and has not been tested extensively.

Expects texture names like:

* `/Brick`
    * `Brick_Color.png`
    * `Brick_Bump.png`
    * `Brick_Normal.png`
...

## Supported Channels:

* Color
* Luminance
* Bump
* Displacement
* Ambient Occlusion
* Normal

## To Do

* [ ] Add Roughness support
* [ ] Add Reflection support
* [ ] Add Metalness support
* [ ] Textures for multiple materials across mutliple directories
* [ ] Non-standard materials (e.g. PBR materials)
* [ ] Node-Based Material Support
* [ ] Uber Material Support

* [ ] BUG: `*.bmp` textures will be confused for Bump.

## License

Copyright (c) 2019 Donovan Keith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import c4d
from c4d import gui
import os


class ChannelTexture(object):
    def __init__(self, name, channel_id, shader_id, tokens):
        self.name = name
        self.channel_id = channel_id
        self.shader_id = shader_id
        self.tokens = [token.lower() for token in tokens]
        self.texture_path = ""
        self.loaded = False

    def Load(self, mat, texture_dir, texture):
        if not mat or not texture_dir or not texture:
            return False

        # Split filename at "-", " ", or "_"
        chunk_source = texture.lower()
        chunk_source = chunk_source.replace("-", "_")
        chunk_source = chunk_source.replace(" ", "_")
        chunks = chunk_source.split("_")

        # See if any of the chunks match existing tokens
        is_match = False
        for token in self.tokens:
            if token in chunks:
                is_match = True
                break

        if not is_match:
            return False

        # Load texture into Mat
        mat[self.channel_id] = True
        shader = c4d.BaseList2D(c4d.Xbitmap)
        shader[c4d.BITMAPSHADER_FILENAME] = os.path.join(texture_dir, texture)
        mat.InsertShader(shader)
        mat[self.shader_id] = shader

        self.loaded = True

        return True


# Main function
def main():
    texture_dir = c4d.storage.LoadDialog(
        type=c4d.FILESELECTTYPE_IMAGES, title="Select Directory Containing Textures", flags=c4d.FILESELECT_DIRECTORY)
    if texture_dir is None:
        c4d.StatusSetText("Import Textures: Cancelled")
        return

    mat = c4d.BaseMaterial(c4d.Mmaterial)

    channels = [
        ChannelTexture("Color", c4d.MATERIAL_USE_COLOR, c4d.MATERIAL_COLOR_SHADER, [
                       "color", "diffuse", "albedo", "col", "diff", "dif", "clr"]),
        ChannelTexture("Luminance", c4d.MATERIAL_USE_LUMINANCE, c4d.MATERIAL_LUMINANCE_SHADER, [
                       "luminance", "emission", "luma", "lum", "emi"]),
        ChannelTexture("Bump", c4d.MATERIAL_USE_BUMP, c4d.MATERIAL_BUMP_SHADER, [
                       "bump", "bmp"]),  # TODO: Fix possible bug with *.bmp files
        ChannelTexture("Displacement", c4d.MATERIAL_USE_DISPLACEMENT,
                       c4d.MATERIAL_DISPLACEMENT_SHADER, ["displacement", "disp", "height"]),
        ChannelTexture("Ambient Occlusion", c4d.MATERIAL_USE_DIFFUSION, c4d.MATERIAL_DIFFUSION_SHADER, [
                       "ambientocclusion", "ambient", "AO", "occlusion"]),
        ChannelTexture("Normal", c4d.MATERIAL_USE_DIFFUSION, c4d.MATERIAL_DIFFUSION_SHADER, [
                       "normal", "norm", "nrml", "nrm"])
    ]

    for texture in os.listdir(texture_dir):
        for channel in channels:
            if channel.loaded:
                continue

            channel.Load(mat, texture_dir, texture)

    doc.InsertMaterial(mat)
    c4d.EventAdd()


# Execute main()
if __name__ == '__main__':
    main()

"""Name-en-US: Orient View to Selected Polygon
Description-en-US: Moves and targets camera toward selected polygon.

Version: 1.0.0

## Usage Instructions

1. Select a single polygon on a single object (behavior is unpredictable with more)
2. Run this command.

## Known Limitations

- Doesn't work with multiple objects/polgyons.
- Doesn't evaluate N-Gon/Quad normals
- Will give unpredictable results with non-planar polygons.
- Written in Cinema 4D 26.0, likely won't work with much older versions.
- Code is unsupported, use at your own risk.
- Because I'm using the built-in Frame Selected command, you'll need two undos to undo this script.

## License

The MIT License (MIT)

Copyright (c) 2022, Donovan Keith

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
THE SOFTWARE.
"""

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def error_message(msg="Select a single polygon on a Poly object."):
    c4d.StatusSetText("View to Polygon: [ERROR] ", msg)

def main() -> None:
    if not op:
        return

    if not op.IsInstanceOf(c4d.Opolygon):
        error_message()
        return
        
    polygon_base_select = op.GetPolygonS()
    if not polygon_base_select:
        error_message("No selected polygon.")
    
    poly_count = op.GetPolygonCount()
    if not poly_count:
        error_message("Object has no polygons.")
    
    first_selected = None
    for i, selected in enumerate(polygon_base_select.GetAll(poly_count)):
        if selected:
            first_selected = i
            break
            
    if first_selected is None:
        error_message("No polygons selected.")
    
    points = op.GetAllPoints()
    if not points:
        error_message("Object has no points.")
        
    poly = op.GetPolygon(first_selected)
    a = points[poly.a]
    b = points[poly.b]
    c = points[poly.c]
    
    point_sum = a + b + c
    poly_point_count = 3
    if not poly.IsTriangle():
        point_sum += points[poly.d]
        poly_point_count += 1
        
    center = point_sum / poly_point_count    
    normal = (b-a).Cross(c-b).GetNormalized()
    
    op_mg = op.GetMg()
    center_global = op_mg.Mul(center)
    normal_global = op_mg.MulV(normal)
    
    bd = doc.GetActiveBaseDraw()
    camera = bd.GetEditorCamera()
    
    camera_offset_amount = 500.0
    camera_pos = center_global + normal_global * camera_offset_amount
    camera_to_poly = center_global - camera_pos
    camera_hpb = c4d.utils.VectorToHPB(camera_to_poly)
    camera_mg = c4d.utils.HPBToMatrix(camera_hpb)
    camera_mg.off = camera_pos

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera)
    camera.SetMg(camera_mg)
    c4d.CallCommand(12151) # Frame Selected Objects
    doc.EndUndo()
    c4d.EventAdd()


def state():
    if op and op.IsInstanceOf(c4d.Opolygon):
        return c4d.CMD_ENABLED
    return False

if __name__ == '__main__':
    main()

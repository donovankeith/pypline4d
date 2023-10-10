# pypline4d

A series of utility scripts for Maxon's Cinema 4D (C4D)

| Name | Description |
|------|-------------|
| [generate_docs.py](generate-readme.py) | Creates README.md which lists all .py files in this repo. |

## UI

| Name | Description |
|------|-------------|

## TabletToggle

| Name | Description |
|------|-------------|

## Materials

| Name | Description |
|------|-------------|
| [Make Environment Map](Materials/make-environment-map.py) | Renders an environment map for the selected object. |

## FileIO

| Name | Description |
|------|-------------|
| [Save Incremental++ ...](FileIO/save-incremental.py) | Desciption-en-US: Slightly smarter save incremental. Follows file_v001.txt convention. Supports non-numeric suffixes like `file_v001_first-last.txt` |
| [Merge Files](FileIO/merge-files-in-directory.py) | A script that merges multiple Cinema 4D files into a new project file. |
| [Import Textures as Materials](FileIO/import-textures-as-materials.py) | Select a directory and load the textures. |
| [Print Media in Category](FileIO/print-media-in-category.py) | Prints a list of all media assets belonging to a category ID to the console. |
| [Create RS Material from Textures...](FileIO/create-rs-material-from-textures.py) | Select a texture file to auto-create a Redshift Standard material. |
| [sRGB to ACEScg](FileIO/srgb-to-acescg.py) | Description US: Converts sRGB colors to ACEScg colors. |

## Template

| Name | Description |
|------|-------------|
| [ScriptName](Template/c4d-script-template.py) | Script does these things. |

## Animation

| Name | Description |
|------|-------------|
| [Split Keys](Animation/split-keys.py) | Takes the selected keys and splits them into two keys. |
| [Animate on Spline](Animation/animate-on-spline.py) | Creates an Align To Spline tag with keys at the start/end of animation. |
| [Camera Morph Keys](Animation/camera-morph-keys.py) | Takes first selected CameraMorph tag and automatically add keys based on the |
| [Linear All Keys](Animation/linear-all-keys.py) | Selects all keys and sets them to Linear interpolation |
| [Preview Next Ranged Marker](Animation/next-ranged-marker.py) | Adjust document's preview range to show next named marker with a length. |
| [Spline Clamp All Keys](Animation/spline-clamp-all-keys.py) | Selects all keys and to Smooth and Clamped. |

## Objects

| Name | Description |
|------|-------------|
| [DK-Group Objects By Display Color](Objects/group-by-color.py) | Groups all objects in scene by display color. WARNING |
| [DK-Aim At](Objects/aim-at.py) | Select all objects you want to aim, then select the target before running this command. |
| [Randomize Object Order](Objects/randomize-object-order.py) | Randomizes the order of all top-level objects in your project. |
| [DK-Select Objects By Display Color](Objects/select-by-display-color.py) | Selects Objects with a Similar Display Color |
| [DK-Select Similar Instances](Objects/select-similar-instances.py) | Selects all Instances of the Selected Object(s) |

## Modeling

| Name | Description |
|------|-------------|
| [Compound Boolean Union](Modeling/compound-boole-union.py) | Takes all selected objects, and combines them into a nested boolean hierarchy |
| [Orient View to Selected Polygon](Modeling/orient-view-to-selected-polygon.py) | Moves and targets camera toward selected polygon. |
| [Polys to Window](Modeling/polys-to-window.py) | Converts the currently selected polygon objects to windows |

## C4D Sync

| Name | Description |
|------|-------------|
| [C4D Sync](C4D Sync/c4d-syc.py) | Reroutes Cinema 4D preferences to a directory in your DropBox. |
| [Bake All MoGraph](C4D Sync/bake-all-mograph.py) | Uses standard MoGraph baking commands to bake MoGraph objects. |

## PolyCruncher

| Name | Description |
|------|-------------|
| [Poly Cruncher](PolyCruncher/poly-cruncher.py) | Takes the actively selected object and reduces the polygon count by 90%. |

## Geometry

| Name | Description |
|------|-------------|
| [Copy Length of Selected Edges](Geometry/print-edge-lengths.py) | Copies length of the selected edges to your clipboard. |

## ZeroPSR

| Name | Description |
|------|-------------|
| [Zero PSR](ZeroPSR/zero-psr.py) | Sets Position/Rotation of active objects to (0, 0, 0) and Scale to (1, 1, 1). |
| [Zero Position](ZeroPSR/zero-position.py) | Sets position of active objects to (0, 0, 0) |
| [Zero Scale](ZeroPSR/zero-scale.py) | Despite the name, this sets Scale of active objects to (1, 1, 1). Think of "zero" as "reset". |
| [Zero Rotation](ZeroPSR/zero-rotation.py) | Sets rotation of active objects to (0, 0, 0) |

## NetPrep

| Name | Description |
|------|-------------|
| [NetRender Paths](NetPrep/net-render-paths.py) | NetRender Paths |
| [Update Render Paths](NetPrep/update-render-paths.py) | Update Render Paths |
| [Bake All Mograph](NetPrep/bake-all-mograph.py) | Bake All MoGraph |


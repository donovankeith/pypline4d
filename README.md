# pypline4d

A series of utility scripts for Maxon's Cinema 4D (c4d)## pypline4d

| Name | Description |
|------|-------------|
| [generate_docs.py](generate_readme.py) | Creates README.md which lists all .py files in this repo. |

## UI

| Name | Description |
|------|-------------|

## TabletToggle

| Name | Description |
|------|-------------|

## Materials

| Name | Description |
|------|-------------|
| [Make Environment Map](Materials/MakeEnvironmentMap.py) | Renders an environment map for the selected object. |

## Template

| Name | Description |
|------|-------------|
| [ScriptName](Template/c4d_script_template.py) | Script does these things. |

## Animation

| Name | Description |
|------|-------------|
| [Animate on Spline](Animation/AnimateOnSpline.py) | Creates an Align To Spline tag with keys at the start/end of animation. |
| [Linear All Keys](Animation/LinearAllKeys.py) | Selects all keys and sets them to Linear interpolation |
| [Split Keys](Animation/SplitKeys.py) | Takes the selected keys and splits them into two keys. |
| [Camera Morph Keys](Animation/CameraMorphKeys.py) | Takes first selected CameraMorph tag and automatically add keys based on the |
| [Spline Clamp All Keys](Animation/SplineClampAllKeys.py) | Selects all keys and to Smooth and Clamped. |

## Modeling

| Name | Description |
|------|-------------|
| [Compound Boolean Union](Modeling/CompoundBooleUnion.py) | Takes all selected objects, and combines them into a nested boolean hierarchy |
| [Orient View to Selected Polygon](Modeling/OrientViewToSelectedPolygon.py) | Moves and targets camera toward selected polygon. |
| [Polys to Window](Modeling/PolyToWindow.py) | Converts the currently selected polygon objects to windows |

## C4D Sync

| Name | Description |
|------|-------------|
| [C4D Sync](C4D Sync/c4dsync.py) | Reroutes Cinema 4D preferences to a directory in your DropBox. |
| [Bake All MoGraph](C4D Sync/BakeAllMoGraph.py) | Uses standard MoGraph baking commands to bake MoGraph objects. |

## PolyCruncher

| Name | Description |
|------|-------------|
| [Poly Cruncher](PolyCruncher/PolyCruncher.py) | Takes the actively selected object and reduces the polygon count by 90%. |

## ZeroPSR

| Name | Description |
|------|-------------|
| [Zero Rotation](ZeroPSR/ZeroRotation.py) | Sets rotation of active objects to (0, 0, 0) |
| [Zero Scale](ZeroPSR/ZeroScale.py) | Despite the name, this sets Scale of active objects to (1, 1, 1). Think of "zero" as "reset". |
| [Zero Position](ZeroPSR/ZeroPosition.py) | Sets position of active objects to (0, 0, 0) |
| [Zero PSR](ZeroPSR/ZeroPSR.py) | Sets Position/Rotation of active objects to (0, 0, 0) and Scale to (1, 1, 1). |

## NetPrep

| Name | Description |
|------|-------------|
| [NetRender Paths](NetPrep/NetRenderPaths.py) | NetRender Paths |
| [Update Render Paths](NetPrep/UpdateRenderPaths.py) | Update Render Paths |
| [Bake All Mograph](NetPrep/BakeAllMoGraph.py) | Bake All MoGraph |


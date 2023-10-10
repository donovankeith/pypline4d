"""Name-en-US: Randomize Object Order
Description-en-US: Randomizes the order of all top-level objects in your project.

## Change Log

- v0.1.0: Initial Version

## Known Limitations

- Doesn't properly handle hierarchy.


## Background

I created this script as an object lesson in the importance of naming objects.
Probably only useful to myself and other Teachers.

## License

MIT No Attribution

Copyright 2023 Donovan Keith

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from typing import Optional
import c4d
import random

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    objects = doc.GetObjects()
    print(objects)

    doc.StartUndo()

    random.shuffle(objects)

    for obj in objects:
        doc.AddUndo(c4d.UNDOTYPE_HIERARCHY_PSR, obj)
        obj.Remove()
        doc.InsertObject(obj)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
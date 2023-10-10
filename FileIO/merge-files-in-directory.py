"""Name-en-US: Merge Files
Description-en-US: A script that merges multiple Cinema 4D files into a new project file.
"""

from typing import Optional
import c4d
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def merge_files() -> None:
    # Get directory of files to merge
    directory = c4d.storage.LoadDialog(
        c4d.FILESELECTTYPE_ANYTHING,
        title="Select directory containing files to merge",
        flags=c4d.FILESELECT_DIRECTORY)

    if not directory:
        return

    base_document = c4d.documents.BaseDocument()

    file_paths = [os.path.join(directory, f)
                  for f in os.listdir(directory) if f.endswith('.c4d')]
    file_count = len(file_paths)

    c4d.StatusClear()
    c4d.StatusSetSpin()
    for i, file_path in enumerate(file_paths):
        c4d.StatusSetText(f"Loading [{i+1}/{file_count}]: {file_paths}")
        c4d.documents.MergeDocument(base_document, file_path, c4d.SCENEFILTER_OBJECTS |
                                    c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_MERGESCENE)
    c4d.StatusClear()

    c4d.documents.InsertBaseDocument(base_document)
    c4d.documents.SetActiveDocument(base_document)


def main() -> None:
    merge_files()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()

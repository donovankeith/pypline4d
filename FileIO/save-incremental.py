"""Name-en-US: Save Incremental++ ...
Desciption-en-US: Slightly smarter save incremental. Follows file_v001.txt convention. Supports non-numeric suffixes like `file_v001_first-last.txt`

TODO: Set saved document as the active document
TODO: Retrieve the next AVAILABLE filename
"""

import re
from typing import Optional
import c4d
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def increment_filepath(filepath):
    directory, filename = os.path.split(filepath)
    name, ext = filename.rsplit(".", 1)

    version_token = None
    version_num = None
    digits = None
    prefix = None
    suffix = None

    version_match = re.search(r'(v|ver|version)(\d+)', name)
    num_match = None

    if version_match:
        version_token, version_num = version_match.groups()
        digits = len(version_num)
        prefix, suffix = name.split(version_token + version_num, 1)
    else:
        # If no version token is found, find the last number before the extension
        num_match = re.search(r'(\d+)$', name)
        version_token = ""

        if num_match:
            version_num = num_match.group()
            digits = len(version_num)
            prefix, suffix = name.rsplit(version_num, 1)
        else:
            prefix = name
            suffix = ""

    prefix = prefix
    version_token = version_token if num_match and (
        version_token is not None) else ("v" if prefix.endswith("_") else "_v")
    version_number = int(version_num) if (version_num is not None) else 0
    digits = digits if (digits is not None) else 3
    version_number = str(version_number + 1).rjust(digits,
                                                   '0')  # Increment version numer
    suffix = suffix + "." + ext

    return os.path.join(
        directory,
        prefix + version_token + version_number + suffix
    )


def test_suite():
    assert increment_filepath("file.txt") == "file_v001.txt", "No version info"
    assert increment_filepath(
        "file1.txt") == "file2.txt", "Existing minimal version info, no leading zeros"
    assert increment_filepath("file1.c4d") == "file2.c4d", "Different filetype"
    assert increment_filepath("file10.txt") == "file11.txt", "Multiple digits"
    assert increment_filepath(
        "file_v001.txt") == "file_v002.txt", "Standard form"
    assert increment_filepath(
        "file_v999.txt") == "file_v1000.txt", "Larger numbers"
    assert increment_filepath(
        "file_v01.txt") == "file_v02.txt", "Fewer leading zeros"
    assert increment_filepath(
        "file_v00001.txt") == "file_v00002.txt", "Many leading zeros"
    assert increment_filepath(
        "file_v1.txt") == "file_v2.txt", "Simple version, no leading zeros."
    assert increment_filepath(
        "file_v1_f020.txt") == "file_v2_f020.txt", "Non-version number at end."
    assert increment_filepath(
        "file_v123_vkeith.txt") == "file_v124_vkeith.txt", "User token at end."


def main() -> None:
    test_suite()

    filepath = doc.GetDocumentPath()
    if not filepath:
        filepath = c4d.storage.SaveDialog(
            c4d.FILESELECTTYPE_SCENES, title="PROJECT_v001.c4d", force_suffix="c4d")
    if not filepath:
        return

    incremented_filepath = increment_filepath(filepath)
    c4d.documents.SaveDocument(doc, name=incremented_filepath, saveflags=c4d.SAVEDOCUMENTFLAGS_NONE |
                               c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, format=c4d.FORMAT_C4DEXPORT)


if __name__ == '__main__':
    main()

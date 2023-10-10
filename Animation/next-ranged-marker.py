"""Name-en-US: Preview Next Ranged Marker
Description-en-US: Adjust document's preview range to show next named marker with a length.

Assumptions:

- "Marked Ranges" have a length
- Ranges won't overlap

Known Issues:

* Select non-existent ranges between known ranges.
"""

import c4d
from c4d import gui


def state():
    """Enable if there are some markers in the document."""

    if c4d.documents.GetFirstMarker(doc):
        return True
    else:
        return False


def main():
    cur_time = doc.GetTime()
    first_marker = c4d.documents.GetFirstMarker(doc)

    # Nor markers, so...
    if not first_marker:
        # Set preview range to length of full document.
        doc.SetLoopMinTime(doc.GetMinTime())
        doc.SetLoopMaxTime(doc.GetMaxTime())

    # Build a list of markers
    markers = []
    next_marker = first_marker

    while (next_marker):
        markers.append(next_marker)
        next_marker = next_marker.GetNext()

    # Sort first by marker end time
    markers = sorted(markers, key=lambda m: (
        m[c4d.TLMARKER_TIME] + m[c4d.TLMARKER_LENGTH]))

    # Then sort by marker start time
    markers = sorted(markers, key=lambda m: m[c4d.TLMARKER_TIME])

    ranged_markers = []
    for marker in markers:
        if marker[c4d.TLMARKER_LENGTH].Get() > 0.0:
            ranged_markers.append(marker)

    if not ranged_markers:
        return

    # Find the "next" marker
    loop_min = doc.GetLoopMinTime()
    loop_max = doc.GetLoopMaxTime()

    one_frame = c4d.BaseTime(1.0/float(doc.GetFps()))

    next_ranged_marker = None
    for ranged_marker in ranged_markers:
        range_min = ranged_marker[c4d.TLMARKER_TIME]
        range_max = range_min + ranged_marker[c4d.TLMARKER_LENGTH] - one_frame

        if range_min > loop_max:
            next_ranged_marker = ranged_marker
            break
        elif range_max > loop_max:
            next_ranged_marker = ranged_marker
            break
        elif range_min > loop_min:
            next_ranged_marker = ranged_marker
            break

    if next_ranged_marker is None:
        next_ranged_marker = ranged_markers[0]

    loop_min = next_ranged_marker[c4d.TLMARKER_TIME]
    loop_max = next_ranged_marker[c4d.TLMARKER_TIME] + \
        next_ranged_marker[c4d.TLMARKER_LENGTH] - one_frame

    doc.SetLoopMinTime(loop_min)
    doc.SetLoopMaxTime(loop_max)


# Execute main()
if __name__ == '__main__':
    main()

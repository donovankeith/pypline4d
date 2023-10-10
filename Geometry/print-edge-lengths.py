"""Name-en-US: Copy Length of Selected Edges
Description-en-US: Copies length of the selected edges to your clipboard.
"""

import c4d
from c4d import gui


def IterateSelected(selection, point_count):
    segments = selection.GetSegments()
    for seg in range(0, segments):
        minS, maxS = selection.GetRange(seg, point_count)
        for index in range(minS, maxS+1):
            yield index


def PrintSelectedEdgeIndex(obj):
    if op is None:
        return

    if op.GetType() != c4d.Opolygon:
        return

    max_points_per_poly = 4
    max_point_count = op.GetPolygonCount() * max_points_per_poly
    edge_selection = op.GetEdgeS()

    for index in IterateSelected(edge_selection, max_point_count):
        print("Polygon:", index // 4, "Edge:", index % 4)


def main():
    if op == None:
        return
    if op.GetType() != c4d.Opolygon:
        return

    PrintSelectedEdgeIndex(op)


if __name__ == '__main__':
    main()

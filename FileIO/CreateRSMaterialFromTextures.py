"""Name-en-US: Create RS Material from Textures...
Description-en-US: Select a texture file to auto-create a Redshift Standard material.
"""

import c4d
import maxon


def create_material():
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    if mat is None:
        raise ValueError("Unable to create material.")

    return mat


def create_node_material(node_space_id=None):
    if node_space_id is None:
        node_space_id = c4d.GetActiveNodeSpaceId()
        if node_space_id is None:
            raise ValueError("Unable to get active node space.")

    mat = create_material()
    if mat is None:
        raise ValueError("Unable to create material.")

    node_mat_ref = mat.GetNodeMaterialReference()
    if node_mat_ref is None:
        raise ValueError("Unable to get mat as node material.")

    graph = node_mat_ref.AddGraph(node_space_id)
    if graph is None:
        raise ValueError("Unable to add Grap to material.")

    root = graph.GetRoot()
    if root is None:
        raise ValueError("Unable to get root node.")

    return mat, root


def create_redshift_node_material():
    NODE_SPACE_REDSHIFT = "com.redshift3d.redshift4c4d.class.nodespace"
    mat, root = create_node_material(node_space_id=NODE_SPACE_REDSHIFT)
    if (mat is None) or (root is None):
        raise ValueError(
            "Unable to create redshift node material and retrieve root node.")

    return mat, root


def main():
    mat, root = create_redshift_node_material()
    if (mat is None) or (root is None):
        raise ValueError("Unable to create Redshift Material.")

    doc.StartUndo()

    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
    doc.InsertMaterial(mat)

    for child in root.GetChildren():
        print(child)

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == "__main__":
    main()

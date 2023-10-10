"""Name-en-US: Bake All Mograph
Description-en-US: Bake All MoGraph

by
Donovan Keith

written for C4D v12.048

TO DO:
* Use generic type names instead of specific ID's
"""

import c4d

CLONER = 1018544
CACHE_TAG = 1019337


def is_mograph(obj):
    # Cloner
    if obj.CheckType(1018544):
        return True

    # Matrix
    if obj.CheckType(1018545):
        return True

    # Fracture
    if obj.CheckType(1018791):
        return True

    # MoInstance
    if obj.CheckType(1018957):
        return True

    # MoText
    if obj.CheckType(1019268):
        return True

    # TO DO: Find a way to bake these objects
    # Tracer - Can't bake?
    # MoSpline - Can't bake?

    return False


def insert_cache_tag(cloner):
    """Returns a cache tag that has been inserted onto cloner."""
    if cloner is None:
        return

    # Check to see if a cache tag already exists.
    tags = cloner.GetTags()

    for tag in tags:
        if tag.CheckType(CACHE_TAG):
            return tag

    # If not, create a new one.
    cache_tag = c4d.BaseTag(CACHE_TAG)
    cloner.InsertTag(cache_tag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, cache_tag)

    # Return the tag
    return cache_tag


def bake_cloner(cloner):
    """Creates a MoCache tag, and presses Bake"""

    # Allocate cache tag and add to object.
    cache_tag = insert_cache_tag(cloner)
    c4d.CallButton(cache_tag, c4d.MGCACHETAG_BAKESEQUENCE)


def get_next_object(op):
    """Returns the next object in the scene."""

    if op is None:
        return None

    if op.GetDown():
        return op.GetDown()

    while not op.GetNext() and op.GetUp():
        op = op.GetUp()

    return op.GetNext()


def bake_cloners():
    """Bakes all cloner objects in scene."""

    # Check for objects
    obj = doc.GetFirstObject()
    if obj is None:
        return

    # Make a list of all cloners
    cloners = []
    while obj:
        # If it's a cloner, bake it.
        if is_mograph(obj):
            cloners.append(obj)
        obj = get_next_object(obj)

    # Give meaningful feedback
    count = len(cloners)
    for i, clone in enumerate(cloners):
        c4d.StatusSetText(
            ''.join(("[", str(i+1), "/", str(count), "]: ", clone.GetName())))
        bake_cloner(clone)


def bake_dynamics():
    """Bakes all dynamics body tags in scene."""
    obj = doc.GetFirstObject()
    if obj is None:
        return

    # Make a list of all Dynamics tags
    dynamics_tags = []
    while obj:
        tags = obj.GetTags()
        for tag in tags:
            # Check if it's a dynamics body tag
            if tag.CheckType(180000102):
                dynamics_tags.append(tag)
        obj = get_next_object(obj)

    for dynamics_tag in dynamics_tags:
        print(tag.GetName())
        c4d.CallButton(dynamics_tag, c4d.RIGID_BODY_CACHE_BAKE)


def main():
    doc.StartUndo()
    c4d.StatusSetText('Baking MoGraph.')
    bake_cloners()
    c4d.StatusSetText('Baking Dynamics.')
    bake_dynamics()
    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()

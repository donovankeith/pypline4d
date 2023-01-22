'''Name-en-US: Poly Cruncher
Description-en-US: Takes the actively selected object and reduces the polygon count by 90%.

Written By
Donovan Keith
2011
'''

import c4d
from c4d import gui


def groupObjects():
    print("groupObjects()")
    return c4d.CallCommand(100004772) #Group Objects

def currentStateToObject():
    print("currentStateToObject()")
    return c4d.CallCommand(12233) #Current State to Object

def deleteSelectedObject():
    print("deleteSelectedObject()")
    return c4d.CallCommand(100004787) #Delecte selected Object

def main():
    print("main()")

    #Get Active Object
    doc = c4d.documents.GetActiveDocument()
    if doc is None: return False

    op = doc.GetActiveObject()
    if op is None: return False

    #Save its position
    pred = op.GetPred()
    parent = op.GetUp()

    #Add a Poly Cruncher to Scene
    c4d.CallCommand(1001253) #Poly Reduction
    cruncher = doc.GetActiveObject()
    if cruncher is None:
        print("PolyReduction object was not created")
        return False


    #Reselect Op
    doc.SetActiveObject(op, mode=c4d.SELECTION_ADD)

    #Group the Objects
    groupObjects()

    #Convert to Objects
    currentStateToObject()

    #Delete the Source
    deleteSelectedObject()

    #Select the new Group
    doc.SetActiveObject(doc.GetFirstObject(), mode=c4d.SELECTION_NEW)

    #Expand the new Group and delete the Null
    c4d.CallCommand(100004773) #Expand Object Group
    c4d.CallCommand(100004787) #Delete Active Object

    #Restore its position
    op = doc.GetFirstObject()
    op.Remove()
    doc.InsertObject(op,pred=pred,parent=parent)

    #Delete all material tags
    
    

if __name__=='__main__':
    main()
"""Name-US: NetRender Paths
Description-US: NetRender Paths :: Updates the render save paths to match the file name with no path.

NetRenderPaths v0.2 (August 14, 2011)
copyright Donovan Keith, 2011

License: MIT
 
Written for CINEMA 4D R12.048

KNOWN BUGS:
	Doesn't clean up "Render Settings" names, so if the user has a "/" in the name
	you'll end up with a render error.
"""

import os, sys
import c4d
from c4d import gui
import wave

debug = False

def printName( atom ):
	print(atom.GetName())

def getNextItem( item ):
	if item is None: return None
	
	if item.GetDown(): return item.GetDown()
	
	while not item.GetNext() and item.GetUp():
		item = item.GetUp()
		
	return item.GetNext()

def main():
	"""
	"""
	if debug:
		print("main()")
	
	#Get Doc Path
	doc_path = doc.GetDocumentPath()
	
	#Ensure file is saved
	if doc_path == "":
		gui.MessageDialog("Please save document first.")
		return False
	
	#Get Doc Name
	doc_filename = doc.GetDocumentName()
	doc_name = os.path.splitext( doc_filename )[0]

	#Retrieve the render data
	render_data = doc.GetFirstRenderData()
	
	#Update all render data entries
	while( render_data ):
		render_data[c4d.RDATA_PATH] = doc_name
		render_data[c4d.RDATA_MULTIPASS_FILENAME] = doc_name
		render_data = getNextItem( render_data )
	
	c4d.EventAdd()
	pass
	
if __name__ == "__main__":
	main()
"""Name-en-US: Update Render Paths
Description-en-US: Update Render Paths :: Updates the render save paths to match the file name.

UpdateRenderPaths v0.1 (August 4, 2011)
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
	
	if debug:
		print("doc_name = ", doc_name)
		print("doc_path = ", doc_path)

	#If the "renders" folder doesn't exist, create it.
	renders_path = os.path.join( doc_path, "renders" )
	if not os.path.isdir(renders_path):
		os.mkdir(renders_path)

	#Create a sub-folder for this scene
	render_path = os.path.join(renders_path, doc_name)
	if not os.path.isdir(render_path):
		os.mkdir(render_path)

	#Retrieve the render data
	render_data = doc.GetFirstRenderData()
	
	#Update all render data entries
	while( render_data ):
		rd_name = render_data.GetName().replace(" ","_")
		doc_rd_name = "".join([doc_name, "_", rd_name])
		mp_file_path = os.path.join(render_path, doc_rd_name)
		save_file_path = os.path.join(render_path, "".join([doc_rd_name, "_image"]))
	
	
		render_data[c4d.RDATA_PATH] = save_file_path
		render_data[c4d.RDATA_MULTIPASS_FILENAME] = mp_file_path
		render_data = getNextItem( render_data )
	
	c4d.EventAdd()
	pass
	
if __name__ == "__main__":
	main()
"""
C4D Sync v0.01
Reroutes Cinema 4D preferences to a directory in your DropBox.
Written for CINEMA 4D R14.025

LICENSE:
Copyright (C) 2012 by Donovan Keith (www.donovankeith.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE

INSTRUCTIONS:
Select a camera morph tag.
Run this script.

TO DO:
Multi-select support.
Improve behavior if there are pre-existing keys.

CHANGELOG:
v0.01: Added basic functionality.
v0.02: Added undo, and corrected key spacing. Auto-add
        key even when there are < 2 cameras.

Name-US: Camera Morph Keys
Description-US: Creates a keyframe for each camera in the selected camera morph tag.

import c4d
import os
from c4d import gui
#Welcome to the world of Python

debug = True

def symlink(source, link_name):
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        os_symlink(source, link_name)
    else:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        if csl(link_name, source, flags) == 0:
            raise ctypes.WinError()

def main():
    #gui.MessageDialog('Hello World!')
    
    #Get some default locations
    usr_path_prefs = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_PREFS)
    usr_path_resource = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_RESOURCE)
    usr_path_library = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_LIBRARY_USER)
    usr_path_desktop = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_DESKTOP)
    usr_path_home = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_HOME)
    usr_path_startup = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_STARTUPWRITE)
    usr_path_documents = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_MYDOCUMENTS)

    if debug:
        print usr_path_prefs
        print usr_path_resource
        print usr_path_library
        print usr_path_home
        print usr_path_startup
        print usr_path_home
    
    #Open a file picker
    usr_save_to = c4d.storage.LoadDialog(
        type=c4d.FILESELECTTYPE_ANYTHING,
        title="Where would you like to place your C4D Sync folder?",
        flags=c4d.FILESELECT_DIRECTORY, 
        def_path=usr_path_desktop)
        
    print "User said to save here: ", usr_save_to

    save_to = os.path.join(usr_save_to,"C4D Sync")
    print save_to
    
    print "Creating symlink... ", symlink(usr_path_documents, save_to)

if __name__=='__main__':
    main()
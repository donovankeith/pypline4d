import c4d
from c4d import gui

#Step All Keys

def main():
    #Open Timeline
    c4d.CallCommand(465001513)

    #Select All
    c4d.CallCommand(465001012)

    #Smooth Keys
    c4d.CallCommand(465001003)

    #Clamp Keys
    c4d.CallCommand(465001110)

    #Auto Tangents
    c4d.CallCommand(465001102)

    #Close Window
    c4d.CallCommand(12392)

if __name__=='__main__':
    main()
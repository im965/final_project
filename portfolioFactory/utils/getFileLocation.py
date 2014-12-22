"""
This function creates a pop-up that asks the user to select a file for input

Author: Peter Li
"""

import Tkinter,tkFileDialog

def getFileLocation(msg):
    
    ''' This function opens a GUI that takes in user selection files
    
    Input:
        - msg (str): Message displayed on the top of the window
    
    '''
    
    root = Tkinter.Tk()
    root.withdraw()
    
    filePath = tkFileDialog.askopenfilename(initialdir="./",title = msg)   
    
    return filePath
    
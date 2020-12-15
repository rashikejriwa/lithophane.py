# resize image by slicing the greImageArray
# adjust everything according to base or figure out way in order to adjust z values so that it is never below 3
# easier if everything starts at esentially (0,0,0)

import module_manager
from cmu_112_graphics import *
from PIL import Image
import numpy
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
import math
from stlModel import *
from dynamicCombined3dstl import *
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import os
import copy
import tkinter as tk
from tkinter import filedialog

#global imageFileList
imageFileList = []
imageCount = len(imageFileList)

def appStarted(app):
    app.margin = 70
    app.sideMargin = 20
    app.botomMargin = 50
    app.faces = 1
    app.border = 1
    app.heights = 1
    app.r = 30
    app.facesBool = False
    app.borderBool = False
    app.heightBool = False
    app.facesText = 'Black'
    app.borderText = 'Black'
    app.heightText = 'Black'
    app.facesFill = 'White'
    app.borderFill = 'White'
    app.heightFill = 'White'
    app.saved = False

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    imageFileList.append(filename)
    print(imageFileList)
    imageCount = len(imageFileList)
    print(imageCount)
    
def userInputImage():
    root = tk.Tk()
    button = tk.Button(root, text='Click Here to Upload an Image', command=UploadAction)
    button.pack()
    root.mainloop()

def drawSplash(app, canvas):
    if app.saved == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = 'white')
        canvas.create_text(app.width / 2, app.height / 2, text = 'File Saved to Desktop', font = 'Arial 40 bold')
        canvas.create_text(app.width / 2, app.height / 2 + app.margin, text = 'Press r for to create a new stl', font = 'Arial 40 bold')

def mainScreen(app, canvas):
    r = app.r
    canvas.create_text(app.width / 2, app.margin, text = 'Lithophane.py', font = 'Arial 40 bold')

    canvas.create_text(app.width / 2, app.margin * 2, text = 'Enter Number of Faces', font = 'Arial 20 bold')
    canvas.create_oval(app.width / 2 - r, app.margin * 3 - r, app.width / 2 + r, app.margin * 3 + r, fill = app.facesFill)
    canvas.create_text(app.width / 2, app.margin * 3, text = f'{app.faces}', font = 'Arial 15 bold', fill = app.facesText)

    canvas.create_text(app.width / 2, app.margin * 4, text = 'Enter Border Thickness', font = 'Arial 20 bold')
    canvas.create_oval(app.width / 2 - r, app.margin * 5 - r, app.width / 2 + r, app.margin * 5 + r, fill = app.borderFill)
    canvas.create_text(app.width / 2, app.margin * 5, text = f'{app.border}', font = 'Arial 15 bold', fill = app.borderText)

    canvas.create_text(app.width / 2, app.margin * 6, text = 'Enter Number Enter Model Face Thickness', font = 'Arial 20 bold')
    canvas.create_oval(app.width / 2 - r, app.margin * 7 - r, app.width / 2 + r, app.margin * 7 + r, fill = app.heightFill)
    canvas.create_text(app.width / 2, app.margin * 7, text = f'{app.heights}', font = 'Arial 15 bold', fill = app.heightText)

    canvas.create_text(app.width / 2, app.margin * 8, text = f'Upload Images Below.', font = 'Arial 20 bold')

    canvas.create_rectangle(app.width / 2 - 80, app.height - app.margin - 20, app.width / 2 + 80, app.height - app.margin + 20, fill = 'Black')
    canvas.create_text(app.width / 2, app.height - app.margin, text = 'Save Stl', font = 'Arial 20 bold', fill = 'White')

def drawImagesBoxes(app, canvas):
    n = app.faces
    width = (app.width - 2 * app.sideMargin) / n
    for i in range(n):
        canvas.create_rectangle(i * width + app.sideMargin, app.margin * 8.5, (i + 1) * width + app.sideMargin, app.margin * 10)
        canvas.create_text(i * width + app.sideMargin + width / 2, app.margin * 9, text = '    Click to\nUpload Image')

def mousePressed(app, event):
    x = event.x
    y = event.y
    r = app.r
    if (x > app.width / 2 - r) and (x < app.width / 2 + r) and (y > app.margin * 3 - r) and (y < app.margin * 3 + r):
        app.facesBool,  app.borderBool, app.heightBool = True, False, False
        app.facesText, app.borderText, app.heightText = 'White', 'Black', 'Black'
        app.facesFill, app.borderFill, app.heightFill = 'Black', 'White', 'White'
    elif (x > app.width / 2 - r) and (x < app.width / 2 + r) and (y > app.margin * 5 - r) and (y < app.margin * 5 + r):
        app.facesBool,  app.borderBool, app.heightBool = False, True, False
        app.facesText, app.borderText, app.heightText = 'Black', 'White', 'Black'
        app.facesFill, app.borderFill, app.heightFill = 'White', 'Black', 'White'
    elif (x > app.width / 2 - r) and (x < app.width / 2 + r) and (y > app.margin * 7 - r) and (y < app.margin * 7 + r):
        app.facesBool,  app.borderBool, app.heightBool = False, False, True 
        app.facesText, app.borderText, app.heightText = 'Black', 'Black', 'White'
        app.facesFill, app.borderFill, app.heightFill = 'White', 'White', 'Black'
    else:
        app.facesBool,  app.borderBool, app.heightBool = False, False, False
        app.facesText, app.borderText, app.heightText = 'Black', 'Black', 'Black'
        app.facesFill, app.borderFill, app.heightFill = 'White', 'White', 'White'

    if (x > app.width / 2 - 80) and (x < app.width / 2 + 80) and (y < app.height - app.margin + 20) and (y > app.height - app.margin - 20):
        faceNumberStlModel(imageFileList, app.heights, app.border, app.faces)
        app.saved = True
    
    elif (y > app.margin) * 8.5 and (y < app.margin * 10):
        userInputImage()

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
        global imageFileList
        imageFileList = []
    if app.facesBool:
        if event.key == 'Up':
            app.faces += 1
        elif event.key == 'Down' and app.faces != 1:
            app.faces -= 1
    elif app.borderBool:
        if event.key == 'Up':
            app.border += 1
        elif event.key == 'Down' and app.border != 1:
            app.border -= 1
    elif app.heightBool:
        if event.key == 'Up':
            app.heights += 1
        elif event.key == 'Down' and app.heights != 1:
            app.heights -= 1

def redrawAll(app, canvas):
    mainScreen(app, canvas)
    drawImagesBoxes(app, canvas)
    drawSplash(app, canvas)

def lithophane():
    width = 1200
    height = 800
    runApp(width=width, height=height)

def main():
    lithophane()

if __name__ == '__main__':
    main()

    
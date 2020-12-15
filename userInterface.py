import module_manager
from cmu_112_graphics import *

import math
import os
import copy
import vtk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

from functools import partial

from tkinter.font import Font
from PIL import Image
import numpy
import numpy as np
from stl import mesh

from stlModel import *
from dynamicCombined3dstl import *

lithophane = tk.Tk()
lithophane.configure(bg = '#D9E3E4')
lithophane.geometry('850x685')

######## User Interface Window ########
# creates the main window and frames within this window
margin = 10
modelW, modelH = 650, 450
imageW, imageH = 175, 450
userInputW, userInputH = 825 + margin, 200 
relief = tk.SUNKEN
borderWidth = 5

frameColor = '#606E6C'
modelColor = '#000000'
buttonColor = sliderColor = '#9AA9A7'
labelColor = '#606E6C'
titleColor = '#606E6C'
fontColor = '#000000'
font = Font(family = 'Helvetica', size = 9, weight = 'bold')
titleFont = Font(family = 'Courier', size = 55)
directionsFont = Font(family = 'Helvetica', size = 9, weight = 'bold')

modelFrame = tk.Frame(master = lithophane, width = modelW, height = modelH, relief = relief, borderwidth = borderWidth, bg = modelColor)
imageEditFrame = tk.Frame(master = lithophane, width = imageW, height = imageH, relief = relief, borderwidth = borderWidth, bg = frameColor)
imageInputFrame = tk.Frame(master = lithophane, width = userInputW, height = userInputH, relief = relief, borderwidth = borderWidth, bg = frameColor)

modelFrame.place(x = margin, y = margin)
imageEditFrame.place(x = 650 + 2 * margin, y = margin)
imageInputFrame.place(x = margin, y = modelH + 2 * margin)  

# creates the headings for each of the frames
def frameHeadings():
    titleHeading = tk.Label(master = modelFrame, text = 'LITHOPHANE.PY', background = '#000000', fg = '#9AA9A7', font = titleFont)
    titleHeading.place(x = 30, y = 200)
    titleHeading = tk.Label(master = modelFrame, text = 'To create your 3D lithohane, enter the number of faces, border width, and model height. \nSave your inputs and upload the correct number of images. \nThen, generate your STL file and refresh the model to view your lithophane.', background = '#000000', fg = '#9AA9A7', font = directionsFont)
    titleHeading.place(x = 80, y = 290)

    path = 'titlePicture.jpg'
    global img
    img = Image.open(path)
    img = img.resize((170, 150))
    img = ImageTk.PhotoImage(img)
    cube = tk.Label(master = modelFrame, image = img, width = 150, height = 150, bg = '#000000')
    cube.place(x = 250, y = 40)

    editHeading = tk.Label(master = imageEditFrame, text = 'Using the Features Below,\nCustomize Your Lithophane!', background = labelColor, fg = fontColor, font = font)
    editHeading.place(x = 0, y = 0)

    imageHeading = tk.Label(master = imageInputFrame, text = 'Input Images for Each Face Below', background = labelColor, fg = fontColor, font = font)
    imageHeading.place(x = 5, y = 0)

######## Global Variables ########
imageFileList = []
imageButtonArray = []
faceNum = 1
borderNum = 1
heightNum = 1
faceNumVar = DoubleVar()
borderNumVar = DoubleVar()
heightNumVar = DoubleVar()
img = None
labelImageArray = []

######## Button Functions ########
# this function is called when the save inputs button is pressed
def saveInputs(): 
    global faceNum
    global borderNum
    global heightNum
    global faceNumVar
    global borderNumVar
    global heightNumVar

    faceNum = faceNumVar.get()  
    borderNum = borderNumVar.get() 
    heightNum = heightNumVar.get()

    text = f'Faces: {faceNum}\nBorder: {borderNum}\nHeight: {heightNum}' 
    storedUserInput = tk.Label(master = imageEditFrame, background = labelColor, font = font, fg = fontColor)
    storedUserInput.place(x = 5, y = 290)
    storedUserInput.config(text = text)

# this function is called when the save inputs button is pressed
# the function adds buttons to upload images
def resetImage():
    global imageFileList
    global imageButtonArray
    global labelImageArray
    imageFileList = []
    for label in labelImageArray:
        label.destroy()
    labelImageArray = []
    for button in imageButtonArray:
        button.destroy()
    imageButtonArray = []

def imageUpload():
    global imageFileList
    global imageButtonArray
    global labelImageArray
    global img
    margin = 7

    def uploadImage(index):
        filename = filedialog.askopenfilename()
        imageFileList[index] = filename

        label = labelImageArray[index]
        thickness = 127
        height = 120
        path = imageFileList[index]
        img = Image.open(path)
        img = img.resize((thickness, height))
        img = ImageTk.PhotoImage(img)
        label.configure(image = img, width = thickness, height = height)
        label.image = img

    for i in range(int(faceNum)):  
        thickness = 17
        height = 1

        imageButton = tk.Button(master = imageInputFrame, width = thickness, height = height, command = partial(uploadImage, i), text = 'Upload Image', background = buttonColor, fg = fontColor, font = font)
        imageLabel = tk.Label(master = imageInputFrame, width = thickness, height = height, text = 'No Image', background = labelColor, fg = fontColor, font = font)
        imageButton.place(x = i * 150 + margin, y = 30)
        imageLabel.place(x = i * 150 + margin, y = 60)
        imageButtonArray.append(imageButton)
        labelImageArray.append(imageLabel)
        imageFileList.append(None)
        print(imageButtonArray)

def saveInputCommand():
    saveInputs()
    resetImage()
    imageUpload()

# this function is called when the save stl button is pressed
def saveStlModel():
    global faceNum
    global borderNum
    global heightNum
    global imageFileList
    for i in imageFileList:
        print(i)
    faceNumberStlModel(imageFileList, heightNum, borderNum, faceNum)
    open('lithophane.stl')

# this function is called when the refresh model button is pressed
def generateModel():
    # plotting stl model with vtk is copied from: https://docs.pyvista.org/why.html
    reader = vtk.vtkSTLReader()
    reader.SetFileName("lithophane.stl")

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(reader.GetOutput())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(actor)
    iren.Initialize()
    renWin.Render()
    iren.Start()

    del iren
    del renWin

######## User Interactions (Buttons, Sliders, etc.) ########
# creates the sliders for number of faces, border, and height
# used this documentation to learn how to create a slider: https://www.python-course.eu/tkinter_sliders.php
def userInputs():
    #creates the user input for the number of faces of the 3D geometry
    faceNumHeading = tk.Label(master = imageEditFrame, text = 'Number of Faces', background = labelColor, fg = fontColor, font = font)
    faceNumHeading.place(x = 5, y = 40)
    faceNumScale = Scale(master = imageEditFrame, variable = faceNumVar, from_ = 1, to = 12, orient = HORIZONTAL, background = sliderColor, fg = fontColor, font = font) 
    faceNumScale.place(x = 5, y = 60)

    # creates the user input for the border thickness of each lithophane pannel
    borderNumHeading = tk.Label(master = imageEditFrame, text = 'Border Thickness', background = labelColor, fg = fontColor, font = font)
    borderNumHeading.place(x = 5, y = 110)
    borderNumScale = Scale(master = imageEditFrame, variable = borderNumVar, from_ = 1, to = 20, orient = HORIZONTAL, background = sliderColor, fg = fontColor, font = font) 
    borderNumScale.place(x = 5, y = 130)

    # creates user input for the thickness of each lithophane panel
    heightNumHeading = tk.Label(master = imageEditFrame, text = 'Face Thickness', background = labelColor, fg = fontColor, font = font)
    heightNumHeading.place(x = 5, y = 180)
    heightNumScale = Scale(master = imageEditFrame, variable = heightNumVar, from_ = 1, to = 20, orient = HORIZONTAL, background = sliderColor, fg = fontColor, font = font) 
    heightNumScale.place(x = 5, y = 200)

# creates the buttons for daving inputs, refreshing the model, and saving stl files
def imageEditButtons():
    # inputs are updated and displayed when this button is clicked
    inputButton = tk.Button(master = imageEditFrame, command = saveInputCommand, text = 'Save Inputs', background = buttonColor, fg = fontColor, font = font)
    inputButton.place(x = 5, y = 260)

    # this button will refresh the displayed model when clicked
    refreshModelButton = tk.Button(master = imageEditFrame, command = generateModel, text = 'Refresh the Model', background = buttonColor, fg = fontColor, font = font)
    refreshModelButton.place(x = 5, y = 360)

    # this button saves the stl file to the users desktop
    stlButton = tk.Button(master = imageEditFrame, command = saveStlModel, text = 'Save Your Stl File', background = buttonColor, fg = fontColor, font = font)
    stlButton.place(x = 5, y = 400)

######## Run All Functions ########
def callFunctions():
    frameHeadings()
    imageEditButtons()
    userInputs()

callFunctions()
lithophane.mainloop()

import module_manager
module_manager.review()

from cmu_112_graphics import *
from PIL import Image
import numpy
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
import math
from stlModel import *
from cubeCombined3dstl import *
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# user inputs
def userInput():
    imageDict = dict()
    print('Number of pictures: ')
    imageNum = input()
    for n in range(int(imageNum)):
        print('Give an image path:')
        filename = input()
        createStl(greyScale(filename), n)
        imageDict[n] = n.stl
    return imageDict

border = 5
height = 5
imageFileList = ['images/carnegie.jpg', 'images/gates.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg']
# cubeStlModel(imageFileList, height, border)

def appStarted(app):
    app.margin = 70
    app.sideMargin = app.width / 12
    app.bottomMargin = app.height / 3.5

def mainScreen(app, canvas):
    canvas.create_text(app.width / 2, app.margin, text = 'Lithophane.py', font = 'Arial 40 bold')
    # rectangle for 3d model
    canvas.create_rectangle(app.sideMargin, app.height / 6, app.width * 11/16, app.height - app.bottomMargin)

    #rectangle for images selected
    canvas.create_rectangle(app.width - app.sideMargin, app.height / 6, app.width * 11/16, app.height - app.bottomMargin)

    #rectangle for figure type
    canvas.create_rectangle(app.sideMargin, app.height - app.bottomMargin, app.width - app.sideMargin, app.height - app.margin)

def stlModel(app):
    pass

def redrawAll(app, canvas):
    mainScreen(app, canvas)
    stlModel(app)

def lithophane():
    width = 1200
    height = 800
    runApp(width=width, height=height)

def main():
    lithophane()

if __name__ == '__main__':
    main()

    
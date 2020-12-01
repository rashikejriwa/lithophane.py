import numpy
from stl import mesh
import math
from stlModel import *

#user inputs for a cube shaped file
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

def dimensionsCheck(imageDict):
    xMin, xMax, yMin, yMax, zMin, zMax = None, None, None, None, None, None
    for image in imageDict:
        stlModel = imageDict[image]
        xMinNew, xMaxNew = stlModel.x.min(), stlModel.x.max()
        yMinNew, yMaxNew = stlModel.y.min(), stlModel.y.max()
        zMinNew, zMaxNew = stlModel.z.min(), stlModel.z.max()
        if (xMaxNew < xMax and yMaxNew < yMax) or xMin == None:
            xMin, xMax, yMin, yMax, zMin, zMax = xMinNew, xMaxNew, yMinNew, yMaxNew, zMinNew, zMaxNew
    return xMin, xMax, yMin, yMax, zMin, zMax

############################################################################################################
# by this point all of the images should be the same size
# the stlModel.py program should use the xMin, xMax, yMin, yMax, zMin, zMax values determined in the 
# functions written above to create n stl files of the same dimensions
# add resizing to stlModel.py

def dimensions(stlModel):
    xMin, xMax = stlModel.x.min(), stlModel.x.max()
    yMin, yMax = stlModel.y.min(), stlModel.y.max()
    zMin, zMax = stlModel.z.min(), stlModel.z.max()
    return xMin, xMax, yMin, yMax, zMin, zMax

stlModel1 = mesh.Mesh.from_file('lithophane.stl')
stlModel2 = mesh.Mesh.from_file('lithophane.stl')
stlModel3 = mesh.Mesh.from_file('lithophane.stl')
stlModel4 = mesh.Mesh.from_file('lithophane.stl')

numOfFaces = 4
border = 10

def cubeStlModel(numOfFaces, border):
    angleInc = 360 / numOfFaces

    stlModel1.rotate([0.5, 0, 0], math.radians(angleInc * 0))

    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel2)
    stlModel2.rotate([0.5, 0, 0], math.radians(angleInc * 1))
    stlModel2.y += yMax - border

    stlModel3.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    stlModel3.z -= yMax - border

    stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 2))
    stlModel4.z -= yMax - border
    stlModel4.y += yMax - border

    combined = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data, stlModel4.data]))
    combined.save('combined.stl')

cubeStlModel(numOfFaces, border)


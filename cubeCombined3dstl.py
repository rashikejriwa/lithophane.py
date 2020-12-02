from PIL import Image
import numpy
from stl import mesh
import math
from stlModel import *

# user inputs will be 4 files - the code below will be written assuming they are a list
# uses functions written in the stlModel.py file

# return the minimum dimensions of all of the files inputed
def minImageDimensions(imageFileList):
    imageSizeList = []
    for imageFile in imageFileList:
        filename = imageFile
        greyImageArray = greyScale(filename)
        imageSizeList.append((len(greyImageArray), len(greyImageArray[0])))

    minPixelX = 0
    minPixelY = 0
    minPixelArea = 0
    for imageSize in imageSizeList:
        pixelX = imageSize[0]
        pixelY = imageSize[1]
        pixelArea = pixelX * pixelY
        if (minPixelArea == 0) or (pixelArea < minPixelArea):
            minPixelX = pixelX
            minPixelY = pixelY
            minPixelArea = pixelX * pixelY

    return (minPixelX, minPixelY)

# resizes images and creates the stl models for each resized face/file
def createStlModels(imageFileList):
    stlFaceFiles = []
    (xDimension, yDimension) = minImageDimensions(imageFileList)
    for imageFile in imageFileList:
        image = Image.open(imageFile)
        image = image.resize((xDimension, yDimension))
        image.save('imageFile.jpg')

        imageName = imageFile.split('/')[-1]
        stlName = imageName.split('.')[0]
        stlFaceFiles.append(f'{stlName}.stl')

        createStl(greyScale('imageFile.jpg'), stlName)
    return stlFaceFiles

# gets the dimensions of the stl model
def dimensions(stlModel):
    xMin, xMax = stlModel.x.min(), stlModel.x.max()
    yMin, yMax = stlModel.y.min(), stlModel.y.max()
    zMin, zMax = stlModel.z.min(), stlModel.z.max()
    return xMin, xMax, yMin, yMax, zMin, zMax

# function for creating the cube 3D stl model
def cubeStlModel(imageFileList, numOfFaces, border):
    stlFaceFiles = createStlModels(imageFileList)

    angleInc = 360 / numOfFaces
    stlModel1 = mesh.Mesh.from_file(stlFaceFiles[0])
    stlModel2 = mesh.Mesh.from_file(stlFaceFiles[1])
    stlModel3 = mesh.Mesh.from_file(stlFaceFiles[2])
    stlModel4 = mesh.Mesh.from_file(stlFaceFiles[3])
    # stlModel5 = mesh.Mesh.from_file(stlFaceFiles[4])

    stlModel1.rotate([0.5, 0, 0], math.radians(angleInc * 0))

    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel2)
    stlModel2.rotate([0.5, 0, 0], math.radians(angleInc * 1))
    stlModel2.y += yMax - border

    stlModel3.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    stlModel3.z -= yMax - border

    stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 2))
    stlModel4.z -= yMax - border
    stlModel4.y += yMax - border

    # stlModel5.rotate([0.5, 0, 0], math.radians(angleInc * 0))
    # stlModel5.z -= yMax + border

    cubeStlModel = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data, stlModel4.data]))
    cubeStlModel.save('cubeStlModel.stl')

# function that will allow testing of code without UI but with user inputs
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

# call functions
numOfFaces = 4
border = 5
height = 5

createStl(greyScale(filename), 'cube')
imageFileList = ['images/carnegie.jpg', 'images/gates.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg']

cubeStlModel(imageFileList, numOfFaces, border)




from PIL import Image
import numpy
from stl import mesh
import math
from stlModel import *
import os
import copy

# user inputs will be 4 files - the code below will be written assuming they are a list
# uses functions written in the stlModel.py file

# return the minimum dimensions of all of the files inputed
def minImageDimensions(imageFileList):
    imageSizeList = []
    for imageFile in imageFileList:
        filename = imageFile
        greyImageArray = greyScale(filename)
        imageSizeList.append((len(greyImageArray[0]), len(greyImageArray)))

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
    
    maxPixelX = 100
    maxPixelY = 100
    maxPixelArea = maxPixelX * maxPixelY
    if minPixelArea > maxPixelArea:
        for n in range(101):
            resize = n / 100
            minPixelX *= 1 - resize
            minPixelY *= 1 - resize
            minPixelArea = minPixelX * minPixelY
            if minPixelArea < maxPixelArea:
                return (round(minPixelX), round(minPixelY))
    return (minPixelX, minPixelY)

# resizes images and creates the stl models for each resized face/file
def createStlModels(imageFileList, height, border, numOfFaces):
    stlFaceFiles = []
    (xDimension, yDimension) = minImageDimensions(imageFileList)
    for imageFile in imageFileList:
        image = Image.open(imageFile)
        image = image.resize((xDimension, yDimension))
        image.save('imageFile.jpg')

        imageName = imageFile.split('/')[-1]
        stlName = imageName.split('.')[0]
        stlFaceFiles.append(f'{stlName}.stl')

        createStl(greyScale('imageFile.jpg'), stlName, height, border, numOfFaces)
    return stlFaceFiles

# gets the dimensions of the stl model
def dimensions(stlModel):
    xMin, xMax = stlModel.x.min(), stlModel.x.max()
    yMin, yMax = stlModel.y.min(), stlModel.y.max()
    zMin, zMax = stlModel.z.min(), stlModel.z.max()
    return xMin, xMax, yMin, yMax, zMin, zMax

# takes a user input to create a 3d polygonal prism with that number of faces
def faceNumberStlModel(imageFileList, height, border, numOfFaces):
    stlModelData = []
    if numOfFaces == 1:
        stlFaceFiles = createStlModels(imageFileList, height, border, numOfFaces)  
        stlModel = mesh.Mesh.from_file(stlFaceFiles[0])
        stlModelData.append(stlModel.data)
        stlModel = mesh.Mesh(numpy.concatenate(stlModelData))
    else:
        stlFaceFiles = createStlModels(imageFileList, height, border, numOfFaces)
        angleInc = 360 / numOfFaces
        rotateAngle = angleInc / 2

        for n in range(len(stlFaceFiles)):
            stlModel = mesh.Mesh.from_file(stlFaceFiles[n])
            xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel)
            stlModel.y += - yMax / 2
            stlModel.z += yMax / 2 / math.tan(math.radians(rotateAngle))
            stlModel.rotate([0.5, 0, 0], math.radians(angleInc * n))
            stlModelData.append(stlModel.data)

        stlModel = mesh.Mesh(numpy.concatenate(stlModelData))

    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    stlModel.save(f'{desktop}\lithophane.stl')
    stlModel.save('lithophane.stl')
    print('File Saved')

# use this code to test this file
# imageFileList = [insert list of file paths]
# height = [insert number]
# border = [insert number]
# numOfFaces = [insert number]
# faceNumberStlModel(imageFileList, height, border, numOfFaces)
# print('3D File Saved')

# use this code to test this file
imageFileList = ['images/smallScotty.jpg', 'images/gates.jpg', 'images/smallScotty.jpg', 'images/ece.jpg']
height = 4
border = 2
numOfFaces = 4
faceNumberStlModel(imageFileList, height, border, numOfFaces)
print('3D File Saved')


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
def createStlModels(imageFileList, height, border):
    stlFaceFiles = []
    (xDimension, yDimension) = minImageDimensions(imageFileList)
    for imageFile in imageFileList:
        image = Image.open(imageFile)
        image = image.resize((xDimension, yDimension))
        image.save('imageFile.jpg')

        imageName = imageFile.split('/')[-1]
        stlName = imageName.split('.')[0]
        stlFaceFiles.append(f'{stlName}.stl')

        createStl(greyScale('imageFile.jpg'), stlName, height, border)
    return stlFaceFiles

# gets the dimensions of the stl model
def dimensions(stlModel):
    xMin, xMax = stlModel.x.min(), stlModel.x.max()
    yMin, yMax = stlModel.y.min(), stlModel.y.max()
    zMin, zMax = stlModel.z.min(), stlModel.z.max()
    return xMin, xMax, yMin, yMax, zMin, zMax

# function for creating the cube 3D stl model
def cubeStlModel(imageFileList, height, border):
    stlFaceFiles = createStlModels(imageFileList, height, border)

    numOfFaces = 4
    angleInc = 360 / numOfFaces
    stlModel1 = mesh.Mesh.from_file(stlFaceFiles[0])
    stlModel2 = mesh.Mesh.from_file(stlFaceFiles[1])
    stlModel3 = mesh.Mesh.from_file(stlFaceFiles[2])
    stlModel4 = mesh.Mesh.from_file(stlFaceFiles[3])
    # stlModel5 = mesh.Mesh.from_file(stlFaceFiles[4])

    stlModel1.rotate([0.5, 0, 0], math.radians(angleInc * 0))

    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel2)
    stlModel2.rotate([0.5, 0, 0], math.radians(angleInc * 1))
    stlModel2.y += yMax - border - (height - border)

    stlModel3.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    stlModel3.z -= yMax - border - (height - border)

    stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 2))
    stlModel4.z -= yMax - border - (height - border)
    stlModel4.y += yMax - border - (height - border)

    # stlModel5.rotate([0.5, 0, 0], math.radians(angleInc * 0))
    # stlModel5.z -= yMax + border

    cubeStlModel = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data, stlModel4.data]))
    cubeStlModel.save('cubeStlModel.stl')

def hexagonalStlModel(imageFileList, height, border):
    stlFaceFiles = createStlModels(imageFileList, height, border)

    numOfFaces = 6
    angleInc = 360 / numOfFaces
    stlModel1 = mesh.Mesh.from_file(stlFaceFiles[0])
    stlModel2 = mesh.Mesh.from_file(stlFaceFiles[1])
    stlModel3 = mesh.Mesh.from_file(stlFaceFiles[2])
    stlModel4 = mesh.Mesh.from_file(stlFaceFiles[3])
    stlModel5 = mesh.Mesh.from_file(stlFaceFiles[4])
    stlModel6 = mesh.Mesh.from_file(stlFaceFiles[5])

    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel1)

    stlModel1.rotate([0.5, 0, 0], math.radians(angleInc * 0))
    stlModel1.y += - xMax + border

    stlModel2.rotate([0.5, 0, 0], math.radians(angleInc * 1))
    
    stlModel3.rotate([0.5, 0, 0], math.radians(angleInc * 2))
    stlModel3.z += - xMax * math.sin(angleInc * math.pi / 180)
    stlModel3.y += xMax * math.cos(angleInc * math.pi / 180)

    stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    stlModel4.z += - 2 * xMax * math.sin(angleInc * math.pi / 180)

    stlModel5.rotate([0.5, 0, 0], math.radians(angleInc * 4))
    stlModel5.y += - xMax + border
    stlModel5.z += - 2 * xMax * math.sin(angleInc * math.pi / 180)
    
    stlModel6.rotate([0.5, 0, 0], math.radians(angleInc * 5))
    stlModel6.y += - yMax - xMax * math.cos(angleInc * math.pi / 180) + border
    stlModel6.z += - xMax * math.sin(angleInc * math.pi / 180)

    cubeStlModel = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data, stlModel4.data, stlModel5.data, stlModel6.data]))
    cubeStlModel.save('hexagonalStlModel.stl')

def faceNumberStlModel(imageFileList, height, border):
    stlFaceFiles = createStlModels(imageFileList, height, border)

    numOfFaces = 3
    angleInc = 360 / numOfFaces
    stlModel1 = mesh.Mesh.from_file(stlFaceFiles[0])
    stlModel2 = mesh.Mesh.from_file(stlFaceFiles[1])
    stlModel3 = mesh.Mesh.from_file(stlFaceFiles[2])
    stlModel4 = mesh.Mesh.from_file(stlFaceFiles[3])
    #stlModel5 = mesh.Mesh.from_file(stlFaceFiles[4])

    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel1)

    stlModel1.rotate([0, 0, 0.5], math.radians(angleInc * 0))
    #stlModel1.y += - xMax #+ abs(height * math.cos(math.radians(30)))

    stlModel2.rotate([0, 0, 0.5], math.radians(angleInc * 1))
    

    stlModel3.rotate([0, 0, 0.5], math.radians(angleInc * 2))
    #stlModel3.z += - xMax * math.sin(math.radians(angleInc))  
    #stlModel3.y += xMax * math.cos(math.radians(angleInc)) 

    # stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    # stlModel4.z += - 2 * xMax * math.sin(angleInc * math.pi / 180)

    # stlModel5.rotate([0.5, 0, 0], math.radians(angleInc * 4))
    # stlModel5.y += - xMax + border
    # stlModel5.z += - 2 * xMax * math.sin(angleInc * math.pi / 180)
    
    # stlModel6.rotate([0.5, 0, 0], math.radians(angleInc * 5))
    # stlModel6.y += - yMax - xMax * math.cos(angleInc * math.pi / 180) + border
    # stlModel6.z += - xMax * math.sin(angleInc * math.pi / 180)

    cubeStlModel = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data]))
    cubeStlModel.save('faceNumberStlModel.stl')

def test(imageFileList, height, border):
    stlFaceFiles = createStlModels(imageFileList, height, border)

    numOfFaces = 4
    angleInc = 360 / numOfFaces
    rotateAngle = angleInc / 2
    stlModel1 = mesh.Mesh.from_file(stlFaceFiles[0])
    stlModel2 = mesh.Mesh.from_file(stlFaceFiles[1])
    stlModel3 = mesh.Mesh.from_file(stlFaceFiles[2])
    stlModel4 = mesh.Mesh.from_file(stlFaceFiles[3])
    xMin, xMax, yMin, yMax, zMin, zMax = dimensions(stlModel1)

    stlModel1.y += - yMax / 2
    stlModel1.z += yMax / 2 / math.tan(math.radians(rotateAngle))
    stlModel1.rotate([0.5, 0, 0], math.radians(angleInc * 0))

    stlModel2.y += - yMax / 2
    stlModel2.z += yMax / 2 / math.tan(math.radians(rotateAngle))
    stlModel2.rotate([0.5, 0, 0], math.radians(angleInc * 1))

    stlModel3.y += - yMax / 2
    stlModel3.z += yMax / 2 / math.tan(math.radians(rotateAngle))
    stlModel3.rotate([0.5, 0, 0], math.radians(angleInc * 2))

    stlModel4.y += - yMax / 2
    stlModel4.z += yMax / 2 / math.tan(math.radians(rotateAngle))
    stlModel4.rotate([0.5, 0, 0], math.radians(angleInc * 3))
    # stlModel2.y += - yMax / 2
    # stlModel2.x += - yMax / 2 / math.tan(math.radians(60))
    # stlModel3.y += - yMax / 2
    # stlModel3.x += - yMax / 2 / math.tan(math.radians(60))

    # stlModel1.rotate([0, 0, 0.5], math.radians(angleInc * 0))
    # stlModel2.rotate([0, 0, 0.5], math.radians(angleInc * 1))
    # stlModel3.rotate([0, 0, 0.5], math.radians(angleInc * 2))

    cubeStlModel = mesh.Mesh(numpy.concatenate([stlModel1.data, stlModel2.data, stlModel3.data, stlModel4.data]))
    cubeStlModel.save('faceNumberStlModel.stl')

border = 5
height = 10
imageFileList = ['images/carnegie.jpg', 'images/gates.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg']
#hexagonalStlModel(imageFileList, height, border)
#faceNumberStlModel(imageFileList, height, border)
test(imageFileList, height, border)


# this file generates one stl model of a given image with the desired height and border thickness
from PIL import Image
import numpy as np
from stl import mesh
import math
import copy

# takes in an image and converts it to black and white
def greyScale(filename):
    image = Image.open(filename)
    greyImage = image.convert('L')
    # array of [row, row, row ...], row is a list of [col, col, col ...]
    # array is [[col, col ...], [col, col ...] ...]
    greyImageArray = np.asarray(greyImage) 
    return greyImageArray

def createTriFace(faceList):
    sideFace = faceList
    northFace1 = np.array([sideFace[2], sideFace[6], sideFace[4]])
    northFace2 = np.array([sideFace[4], sideFace[0], sideFace[2]]) 

    eastFace1 = np.array([sideFace[3], sideFace[7], sideFace[6]])
    eastFace2 = np.array([sideFace[6], sideFace[2], sideFace[3]])

    southFace1 = np.array([sideFace[7], sideFace[5], sideFace[1]])
    southFace2 = np.array([sideFace[1], sideFace[3], sideFace[7]]) 

    westFace1 = np.array([sideFace[0], sideFace[4], sideFace[5]])
    westFace2 = np.array([sideFace[5], sideFace[1], sideFace[0]]) 

    return northFace1, northFace2, eastFace1, eastFace2, southFace1, southFace2, westFace1, westFace2 

# function creates a singualar stl to be put together in the dynamicCombined3dstl.py file
# if there are more than 2 faces as the user input, additional faces are added to the stl
def createStl(greyImageArray, stlFileName, height, border, numOfFaces):  
    height = int(height)
    border = int(border)
    numOfFaces = int(numOfFaces)
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])
    vertices = [[0] * (pixelY - border) for pixel in range(pixelX - border)]
    faces = []

    # creates the top face of the lithophane based on the value in the grey scale image array
    # each image pixel is defined using x pixel location, y pixel location, and z as a fraction of the user input height
    # generates top surface mesh by creating 2 triangular faces per pixel
    for x in range(border, pixelX - border):
        for y in range(border, pixelY - border):
            z = greyImageArray[x][y]
            vertices[x][y] = (x, y, height - (height * z / 255))

    for x in range(border, pixelX - 1 - border):
        for y in range(border, pixelY - 1 - border):
            triVertA = vertices[x][y]
            triVertB = vertices[x + 1][y]
            triVertC = vertices[x + 1][y + 1]
            triVertD = vertices[x][y + 1]

            triFace1 = np.array([triVertA, triVertB, triVertC])
            triFace2 = np.array([triVertC, triVertD, triVertA])         
            faces.append(triFace1)
            faces.append(triFace2)

    # creates the flat bottom surface of the lithophane 
    base = 0.1
    bottomFace = [[0, 0, 0], [0, pixelY, 0], [pixelX, 0, 0], [pixelX, pixelY, 0],
                [border, border, base], [border, pixelY - border, base], [pixelX - border, border, base], [pixelX - border, pixelY - border, base]]

    # for x in range(border, pixelX - 1 - border):
    #     triVertA = (x, border, 0)
    #     triVertB = (x, border, vertices[x][0])
    #     triVertC = (x + 1, border, 0)
    #     faces.append([triVertA, triVertB, triVertC])
    
    # top and bottom faces of base
    bottomFace1 = [bottomFace[3], bottomFace[1], bottomFace[0]]
    bottomFace2 = [bottomFace[0], bottomFace[2], bottomFace[3]]
    bottomFace3 = [bottomFace[7], bottomFace[5], bottomFace[4]]
    bottomFace4 = [bottomFace[4], bottomFace[6], bottomFace[7]]
    faces.append(bottomFace1)
    faces.append(bottomFace2)
    faces.append(bottomFace3)
    faces.append(bottomFace4)
    
    # creates the side surfaces of the lithophane
    sideFace = [[0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height],
                [0, 0, 0], [pixelX, 0, 0], [0, pixelY, 0], [pixelX, pixelY, 0]]

    for triFace in createTriFace(sideFace):
        faces.append(triFace)
    
    # creates the inner border of the lithophane
    borderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height],
                [border, border, base], [pixelX - border, border, base], [border, pixelY - border, base], [pixelX - border, pixelY - border, base]]
    
    for triFace in createTriFace(borderFace):
        faces.append(triFace)
    
    # creates the top face of the lithophane border
    innerTopBorderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height]]
    outerTopBorderFace = [[0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height]]

    # left pannel
    borderSide1 = [[0, border, height], outerTopBorderFace[0], outerTopBorderFace[1]]
    borderSide2 = [outerTopBorderFace[1], [pixelX, border, height], [0, border, height]]
    # right pannel
    borderSide3 = [outerTopBorderFace[3], outerTopBorderFace[2], [0, pixelY - border, height]]
    borderSide4 = [[0, pixelY - border, height], [pixelX, pixelY - border, height], outerTopBorderFace[3]]
    # top pannel
    borderSide5 = [[0, border, height], innerTopBorderFace[0], innerTopBorderFace[2]]
    borderSide6 = [innerTopBorderFace[2], [0, pixelY - border, height], [0, border, height]]
    # bottom pannel
    borderSide7 = [innerTopBorderFace[1], [pixelX, border, height], [pixelX, pixelY - border, height]]
    borderSide8 = [[pixelX, pixelY - border, height], [pixelX - border, pixelY - border, height],innerTopBorderFace[1]]

    faces.append(borderSide1)
    faces.append(borderSide2)
    faces.append(borderSide3)
    faces.append(borderSide4)
    faces.append(borderSide5)
    faces.append(borderSide6)
    faces.append(borderSide7)
    faces.append(borderSide8)

    # creates connections between stls when larger than 2 images
    if numOfFaces > 2:
        # adds connections between stl files in the form of a trianglular prism
        angleInc = 360 / numOfFaces
        translateAngle = math.radians(180 - angleInc)

        triVertices1 = [(pixelX, 0, 0), (pixelX, 0, height),(pixelX, - height * math.sin(translateAngle), - height * math.cos(translateAngle))]
        triVertices2 = [(0, 0, 0), (0, 0, height),(0, - height * math.sin(translateAngle), - height * math.cos(translateAngle))]

        # one side triangle
        triFace1 = [triVertices1[1], triVertices1[2], triVertices1[0]]
        # other side triangle
        triFace2 = [triVertices2[2], triVertices2[1], triVertices2[0]]
        # one flat face
        triFace3 = [triVertices1[2], triVertices1[1], triVertices2[2]]
        triFace4 = [triVertices1[1], triVertices2[1], triVertices2[2]]
        # second flat face
        triFace5 = [triVertices1[1], triVertices1[0], triVertices2[0]]
        triFace6 = [triVertices2[0], triVertices2[1], triVertices1[1]]
        # third flat face
        triFace7 = [triVertices2[0], triVertices1[0], triVertices1[2]]
        triFace8 = [triVertices1[2], triVertices2[2], triVertices2[0]]

        faces.append(triFace1)
        faces.append(triFace2)
        faces.append(triFace3)
        faces.append(triFace4)
        faces.append(triFace5)
        faces.append(triFace6)
        faces.append(triFace7)
        faces.append(triFace8)

        # adds the connections triangles needed to create the printing surface
        printAngle = math.radians(180 / numOfFaces)
        triPrintSurf = [(border, 0, 0), (border, pixelY, 0), (border, pixelY / 2, - (pixelY) / (2 * math.tan(printAngle))), 
                        (0, 0, 0), (0, pixelY, 0), (0, pixelY / 2, - (pixelY) / (2 * math.tan(printAngle)))]

        # one flat face
        printSurf1 = [triPrintSurf[4], triPrintSurf[5], triPrintSurf[2]]
        printSurf2 = [triPrintSurf[2], triPrintSurf[1], triPrintSurf[4]]
        # second flat face
        printSurf3 = [triPrintSurf[1], triPrintSurf[4], triPrintSurf[3]]
        printSurf4 = [triPrintSurf[3], triPrintSurf[0], triPrintSurf[1]]
        # third flat face
        printSurf5 = [triPrintSurf[5], triPrintSurf[3], triPrintSurf[0]]
        printSurf6 = [triPrintSurf[0], triPrintSurf[2], triPrintSurf[5]]
        
        printSurf7 = [triPrintSurf[2], triPrintSurf[1], triPrintSurf[0]]
        printSurf8 = [triPrintSurf[5], triPrintSurf[4], triPrintSurf[3]]

        faces.append(printSurf1) 
        faces.append(printSurf2)
        faces.append(printSurf3) 
        faces.append(printSurf4)
        faces.append(printSurf5) 
        faces.append(printSurf6)
        faces.append(printSurf7) 
        faces.append(printSurf8)

    facesArray = np.array(faces)
    lithophane = mesh.Mesh(np.zeros(facesArray.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane.vectors[i][j] = facesArray[i][j]
    
    lithophane.save(f'{stlFileName}.stl')

# use code below for testing this
# filename = 'images/scotty.jpg'
# greyImageArray = greyScale(filename)
# height = 4
# border = 2
# numOfFaces = 1
# stlFileName = 'test'
# createStl(greyImageArray, stlFileName, height, border, numOfFaces)
# print('saved')

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

def createCube(face):
    face1 = [face[3], face[1], face[0]]
    face2 = [face[0], face[2], face[3]]
    face3 = [face[7], face[5], face[4]]
    face4 = [face[4], face[6], face[7]]

    face5 = [face[4], face[0], face[2]]
    face6 = [face[2], face[6], face[4]]
    face7 = [face[6], face[2], face[3]]
    face8 = [face[3], face[7], face[6]]
    face9 = [face[7], face[1], face[3]]
    face10 = [face[1], face[5], face[7]]
    face11 = [face[5], face[1], face[0]]
    face12 = [face[0], face[4], face[5]]

    faces = [face1, face2, face3, face4, face5, face6, face7, face8, face9, face10, face11, face12]
    return faces

# function creates a singualar stl to be put together in the dynamicCombined3dstl.py file
# if there are more than 2 faces as the user input, additional faces are added to the stl
def createStl(greyImageArray, stlFileName, height, border, numOfFaces):  
    height = int(height)
    border = int(border)
    numOfFaces = int(numOfFaces)
    # resizes the images after subtracting the border pixels
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])
    vertices = [[0] * (pixelY - border) for pixel in range(pixelX - border)]
    faces = []
    base = 0.1
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

    overlap = 1
    gap = overlap + 1
    
    bottomFace = [[0, 0, 0], [0, pixelY, 0], [pixelX, 0, 0], [pixelX, pixelY, 0],
                [0, 0, base], [0, pixelY, base], [pixelX, 0, base], [pixelX, pixelY, base]]
    bottomFaceList = createCube(bottomFace)

    for triFace in bottomFaceList:
        faces.append(triFace)
    
    # creates the side surfaces of the lithophane
    leftFace = [[0, 0, base], [0, pixelY, base], [border + overlap, 0, base],  [border + overlap, pixelY, base],
                [0, 0, height], [0, pixelY, height], [border + overlap, 0, height], [border + overlap, pixelY, height]]
    for triFace in createCube(leftFace):
        faces.append(triFace)

    # creates the side surfaces of the lithophane
    rightFace = [[pixelX - border - gap, 0, base], [pixelX - border - gap, pixelY, base], [pixelX, 0, base],  [pixelX, pixelY, base],
                [pixelX - border - gap, 0, height], [pixelX - border - gap, pixelY, height], [pixelX, 0, height], [pixelX, pixelY, height]]
    for triFace in createCube(rightFace):
        faces.append(triFace)

    frontFace = [[border, 0, base], [border, border + gap, base], [pixelX - border, 0, base],  [pixelX - border, border + gap, base],
                [border, 0, height], [border, border + gap, height], [pixelX - border, 0, height],  [pixelX - border, border + gap, height]]
    for triFace in createCube(frontFace):
        faces.append(triFace)

    backFace = [[border, pixelY - border - overlap, base], [border, pixelY, base], [pixelX - border, pixelY - border - overlap, base],  [pixelX - border, pixelY, base],
                [border, pixelY - border - overlap, height], [border, pixelY, height], [pixelX - border, pixelY - border - overlap, height],  [pixelX - border, pixelY, height]]
    for triFace in createCube(backFace):
        faces.append(triFace)

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

    # lines 161 - 168 moderately modified from https://pypi.org/project/numpy-stl/
    facesArray = np.array(faces)
    lithophane = mesh.Mesh(np.zeros(facesArray.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane.vectors[i][j] = facesArray[i][j]
    
    lithophane.save(f'{stlFileName}.stl')
    return faces
    
# use this code to test this file
# filename = [file path to an image as a string]
# greyImageArray = greyScale(filename)
# height = [insert number]
# border = [insert number]
# numOfFaces = [insert number]
# stlFileName = [insert string]
# createStl(greyImageArray, stlFileName, height, border, numOfFaces)
# print('Single 3D File Saved')

#use code below for testing this
# filename = 'images/scotty.jpg'
# greyImageArray = greyScale(filename)
# height = 4
# border = 2
# numOfFaces = 1
# stlFileName = 'lithophane'
# createStl(greyImageArray, stlFileName, height, border, numOfFaces)
# print('Single 3D File Saved')


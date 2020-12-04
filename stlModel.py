# this file generates one stl model of a given image with the desired height and border thickness
from PIL import Image
import numpy as np
from stl import mesh
import math

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

def addTriEdges(height, border, numOfFaces):
    pass

def createStl(greyImageArray, stlFileName, height, border, numOfFaces):  
    # creates the top surface of the lithophane 
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])

    vertices = [([0] * pixelY) for pixel in range(pixelX)]
    for x in range(pixelX):
        for y in range(pixelY):
            z = greyImageArray[x][y]
            vertices[x][y] = (x, y, height - (height * z / 255))

    faces = []
    for x in range(pixelX - 1):
        for y in range(pixelY - 1):
            triVertA = vertices[x][y]
            triVertB = vertices[x + 1][y]
            triVertC = vertices[x + 1][y + 1]
            triVertD = vertices[x][y + 1]

            triFace1 = np.array([triVertA, triVertB, triVertC])
            triFace2 = np.array([triVertC, triVertD, triVertA])         
            faces.append(triFace1)
            faces.append(triFace2)
    
    # creates the flat bottom surface of the lithophane
    bottomFace = [[0, 0, 0], [0, pixelY, 0], [pixelX, 0, 0], [pixelX, pixelY, 0]]
    bottomFace1 = [bottomFace[0], bottomFace[1], bottomFace[3]]
    bottomFace2 = [bottomFace[3], bottomFace[2], bottomFace[0]]
    faces.append(bottomFace1)
    faces.append(bottomFace2)

    # creates the side surfaces of the lithophane
    sideFace = [[0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height],
                [0, 0, 0], [pixelX, 0, 0], [0, pixelY, 0], [pixelX, pixelY, 0]]

    for triFace in createTriFace(sideFace):
        faces.append(triFace)

    # creates the inner border of the lithophane
    borderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height],
                [border, border, 0], [pixelX - border, border, 0], [border, pixelY - border, 0], [pixelX - border, pixelY - border, 0]]
    
    for triFace in createTriFace(borderFace):
        faces.append(triFace)

    # creates the top face of the lithophane
    topBorderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height],
                    [0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height]]
    
    for triFace in createTriFace(topBorderFace):
        faces.append(triFace) 

    # creates connections between stls when larger than 2 images
    if numOfFaces > 2:
        # adds connections between stl files in the form of a trianglular prism
        angleInc = 360 / numOfFaces
        translateAngle = math.radians(180 - angleInc)

        triVertices1 = [(pixelX, 0, 0), (pixelX, 0, height),(pixelX, - height * math.sin(translateAngle), - height * math.cos(translateAngle))]
        triVertices2 = [(0, 0, 0), (0, 0, height),(0, - height * math.sin(translateAngle), - height * math.cos(translateAngle))]

        triFace1 = [triVertices1[2], triVertices1[1], triVertices1[0]]
        triFace2 = [triVertices2[2], triVertices2[1], triVertices2[0]]
        triFace3 = [triVertices1[2], triVertices1[1], triVertices2[2]]
        triFace4 = [triVertices1[1], triVertices2[1], triVertices2[2]]

        faces.append(triFace1)
        faces.append(triFace2)
        faces.append(triFace3)
        faces.append(triFace4)

        # # adds the connections triangles needed to create the printing surface
        printAngle = math.radians(angleInc / 2)
        triPrintSurf1 = [(height, 0, 0), (height, pixelY, 0), (height, pixelY / 2, - pixelX / 2 / math.tan(printAngle))]
        triPrintSurf2 = [(0, 0, 0), (0, pixelY, 0), (0, pixelY / 2, - pixelX / 2 / math.tan(printAngle))]

        printSurf1 = [triPrintSurf1[0], triPrintSurf1[1], triPrintSurf1[2]]
        printSurf2 = [triPrintSurf2[0], triPrintSurf2[1], triPrintSurf2[2]]

        faces.append(printSurf1) 
        faces.append(printSurf2)

    facesArray = np.array(faces)
    lithophane = mesh.Mesh(np.zeros(facesArray.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane.vectors[i][j] = facesArray[i][j]
    
    lithophane.save(f'{stlFileName}.stl')


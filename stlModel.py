# this file generates one stl model of a given image with the desired height and border thickness
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh

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

def createStl(greyImageArray, stlFileName, height, border):  
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
    bottomFace2 = [bottomFace[0], bottomFace[2], bottomFace[3]]
    faces.append(bottomFace1)
    faces.append(bottomFace2)

    # creates the side surfaces of the lithophane
    sideFace = [[0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height],
                [0, 0, 0], [pixelX, 0, 0], [0, pixelY, 0], [pixelX, pixelY, 0]]

    for triFace in createTriFace(sideFace):
        faces.append(triFace)

    #creates the inner border of the lithophane
    borderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height],
                [border, border, 0], [pixelX - border, border, 0], [border, pixelY - border, 0], [pixelX - border, pixelY - border, 0]]
    
    for triFace in createTriFace(borderFace):
        faces.append(triFace)

    #creates the top face of the lithophane
    topBorderFace = [[border, border, height], [pixelX - border, border, height], [border, pixelY - border, height], [pixelX - border, pixelY - border, height],
                    [0, 0, height], [pixelX, 0, height], [0, pixelY, height], [pixelX, pixelY, height]]
    
    for triFace in createTriFace(topBorderFace):
        faces.append(triFace) 

    facesArray = np.array(faces)
    lithophane = mesh.Mesh(np.zeros(facesArray.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane.vectors[i][j] = facesArray[i][j]
    
    lithophane.save(f'{stlFileName}.stl')


border = 5
height = 5
imageFileList = ['images/carnegie.jpg', 'images/gates.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg', 'images/smallScotty.jpg']
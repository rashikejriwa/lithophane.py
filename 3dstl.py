from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh

#possible user inputs
filename = 'images/smallerScotty.jpg'
thickness= 255

# takes in an image and converts it to black and white
def greyScale(filename):
    image = Image.open(filename)
    greyImage = image.convert('L')
    # array of [row, row, row ...], row is a list of [col, col, col ...]
    # array is [[col, col ...], [col, col ...] ...]
    greyImageArray = np.asarray(greyImage) 
    plt.axis('off')
    plt.imshow(greyImage, cmap = 'gray')
    plt.show()
    return greyImageArray

def createStl(greyImageArray):
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])

    vertices = np.zeros((pixelX, pixelY, 3)) #pixel location interms of row nad col with greyImageArray value
    for x in range(pixelX):
        for y in range(pixelY):
            z = greyImageArray[x][y]
            vertices[x][y] = (x, y, thickness - z)

    faces = []
    for x in range(pixelX - 1):
        for y in range(pixelY - 1):
            triVertA = vertices[x][y]
            triVertB = vertices[x + 1][y]
            triVertC = vertices[x + 1][y + 1]

            triVertD = vertices[x][y]
            triVertE = vertices[x][y + 1]
            triVertF = vertices[x + 1][y + 1]

            triFace1 = np.array([triVertA, triVertB, triVertC])
            triFace2 = np.array([triVertD, triVertE, triVertF])         
            faces.append(triFace1)
            faces.append(triFace2)

    facesArray = np.array(faces)
    lithophane = mesh.Mesh(np.zeros(facesArray.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane.vectors[i][j] = facesArray[i][j]

    lithophane.save(f'lithophane.stl')

greyImageArray = greyScale(filename)
createStl(greyImageArray)





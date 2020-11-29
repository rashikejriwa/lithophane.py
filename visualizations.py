
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#possible user inputs
filename = 'Users\rashi\OneDrive\Desktop\Lithophane.py\images\smallerScotty.jpg'
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

# finds one point for each pixel
def pixelData(greyImageArray):
    pixelList = [] #pixel location interms of row nad col with greyImageArray value
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])
    for x in range(pixelX):
        for y in range(pixelY):
            z = greyImageArray[x][y]
            pixelList.append([x, y, thickness - z])
    return pixelList

print(pixelData(greyScale('images/pixels.jpg')))

# finds the 3 dimensional x, y, z coordinate for each pixel (6 points per pixel)
def pixelData3d(pixelList):
    pixelList3d = []
    for point in pixelList:
        z = point[2]
        additionalPoints = [0, 0, 0], [0, 0, -z], [0, 1, 0], [0, 1, -z], [1, 0, 0], [1, 0, -z], [1, 1, 0], [1, 1, -z]
        for vertex in additionalPoints:
            vertexX = point[0] + vertex[0]
            vertexY = point[1] + vertex[1]
            vertexZ = point[2] + vertex[2]
            pixelList3d.append([vertexX, vertexY, vertexZ])
    return pixelList3d

# creates 3 lists of x, y, and z coordinates for an inputed data set
def xyzPoints(pixelData):
    X, Y, Z = [], [], []
    for point in pixelData:
        X.append(point[0])
        Y.append(point[1])
        Z.append(point[2])
    return X, Y, Z

# creates a 3D scatter plot with one x, y, z coordinate for each pixel
def scatterVisualization(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, c=Z, cmap='twilight_shifted', linewidth=1)
    plt.axis('off')
    plt.show()

# creates a 3D triangular surface plot with one x, y, z coordinate for each pixel
def triSurfVisualization(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z, cmap='twilight_shifted')
    plt.axis('off')
    plt.show()

# call functions
pixelList = pixelData(greyScale(filename))
pixelList3d = pixelData3d(pixelList)
X, Y, Z = xyzPoints(pixelList)
X3d, Y3d, Z3d = xyzPoints(pixelList3d)

scatterVisualization(X, Y, Z)
scatterVisualization(X3d, Y3d, Z3d)

triSurfVisualization(X, Y, Z)
triSurfVisualization(X3d, Y3d, Z3d)




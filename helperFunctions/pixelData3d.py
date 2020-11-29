
#starts with pixel list with x, y, and z for each pixel
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


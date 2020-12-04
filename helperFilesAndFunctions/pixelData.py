
#starts with an image converted to grayscale as an array
thickness= 255 #this can be a user input

# finds one point for each pixel
def pixelData(greyImageArray):
    pixelList = [] #pixel location interms of row nad col with greyImageArray value
    pixelX, pixelY = len(greyImageArray), len(greyImageArray[0])
    for x in range(pixelX):
        for y in range(pixelY):
            z = greyImageArray[x][y]
            pixelList.append([x, y, thickness - z])
    return pixelList

# creates 3 lists of x, y, and z coordinates for an inputed data set
def xyzPoints(pixelData):
    X, Y, Z = [], [], []
    for point in pixelData:
        X.append(point[0])
        Y.append(point[1])
        Z.append(point[2])
    return X, Y, Z
    
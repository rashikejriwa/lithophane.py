import module_manager
module_manager.review()

from cmu_112_graphics import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh

#possible user inputs
filename = 'images/smallerScotty.jpg'
thickness= 255

# call functions
def visualizations():
    pixelList = pixelData(greyScale(filename))
    pixelList3d = pixelData3d(pixelList)
    X, Y, Z = xyzPoints(pixelList)
    X3d, Y3d, Z3d = xyzPoints(pixelList3d)
    scatterVisualization(X, Y, Z)
    scatterVisualization(X3d, Y3d, Z3d)
    triSurfVisualization(X, Y, Z)
    triSurfVisualization(X3d, Y3d, Z3d)

def lithophane():
    width = 200
    height = 200
    runApp(width=width, height=height)

def main():
    lithophane()
    visualizations()

if __name__ == '__main__':
    main()
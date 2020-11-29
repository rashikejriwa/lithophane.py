
#takes in an image and converts it to black and white
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


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

print(greyScale('pixels.jpg'))




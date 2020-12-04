
import matplotlib.pyplot as plt

# creates a 3D scatter plot with one x, y, z coordinate for each pixel
def scatterVisualization(pixelList, X, Y, Z):
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

    
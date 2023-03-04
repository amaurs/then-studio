import numpy
import scipy
from scipy import ndimage


def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return 255 - red, 255 - green, 255 - blue


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red << 16) + (green << 8) + blue

    return RGBint


r = 255

height = 7 * 3 * 3 * 4 * 2 * 5 * 2
width = 3 * 3 * 3 * 3 * 3 * 3

pocket = numpy.zeros((height, width, 3))

for i in range(width):
    g = (i * 255 / width)
    for j in range(height):
        b = (j * 255 / height)
        pocket[j, i] = getRGBfromI(j * width + i)

myset = set(tuple(v) for m2d in pocket for v in m2d)

print(len(myset))

scipy.misc.imsave('pocket.png', pocket)

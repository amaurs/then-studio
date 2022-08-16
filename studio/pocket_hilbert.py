import numpy
import scipy
from scipy import ndimage
import hilbert


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint



width =  4096 # 3 * 3 * 3 * 3 * 2 * 2 * 5
height = 4096 # 3 * 3 * 3 * 3 * 2 * 2 * 7

image_1 = numpy.zeros((height, width, 3))

for i in range(width):
    for j in range(height):

        k = i * height + j
        total = 4096 * 4096  - 1
        cube = hilbert.int_to_Hilbert(total - k,3)
        
        red = cube[0]
        green = cube[1]
        blue = cube[2]

        image_1[j, i] = (red, green, blue)
    


scipy.misc.imsave('pocket_hilbert5.png', image_1)



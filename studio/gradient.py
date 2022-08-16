import numpy
import scipy
from scipy import ndimage


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

r = 256

w = 256
h = 256

width = w * 16
height = h * 16

image_1 = numpy.zeros((height, width, 3))
image_2 = numpy.zeros((height, width, 3))
image_3 = numpy.zeros((height, width, 3))

for k in range(w):
    for l in range(h):
        red = l * w + k
        for i in range(16):
            g = i 
            for j in range(16):
                b = j
                image_1[16 * l + j, 16 * k + i] = (red, g, b)
                image_2[16 * l + j, 16 * k + i] = (g, red, b)
                image_3[16 * l + j, 16 * k + i] = (g, b, red)



scipy.misc.imsave('gradient_1.png', image_1)
scipy.misc.imsave('gradient_2.png', image_2)
scipy.misc.imsave('gradient_3.png', image_3)



import numpy
import scipy
from scipy import ndimage
from scipy.spatial import distance
import random 
import colorsys
import math
import hilbert
w = 10
h = 10

width = 4096
height = 4096


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def getRGBfromI(RGBint):
    Blue =  RGBint & 255
    Green = (RGBint >> 8) & 255
    Red =   (RGBint >> 16) & 255
    return (Red,Green,Blue)

def random_colors():
    colours = []
    for number in range(width*height):
        rgb = getRGBfromI(number)
        colours.append(rgb)
    import random
    random.shuffle(colours)
    return colours







image = numpy.zeros((height, width, 3))

colors = random_colors()
for x in range(width):
    for y in range(height):
        image[x,y] = colors[y * width + x]

scipy.misc.imsave('noise.png', image)



import numpy
import scipy
from scipy import ndimage
import hilbert



# 256 * 256 * 256
# 4096 * 4096

width = 8
height = 8

image_1 = numpy.zeros((height, width, 3))

for k in range(width * height):

    cube = hilbert.int_to_Hilbert(k,3)
    square = hilbert.int_to_Hilbert(k,2)

    red = int(cube[0])
    green = int(cube[1])
    blue = int(cube[2])

    x = int(square[0])
    y = int(square[1])

    print("(%s,%s)" % (x,y))
    print("(%s,%s,%s)" % (red,green,blue))


    image_1[x, y] = (red, green, blue)

    if k%1000==0:
        print(k)



scipy.misc.imsave('hilbert.png', image_1)



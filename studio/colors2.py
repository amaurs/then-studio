import numpy
import scipy
from scipy import ndimage



r = 255

width = 1080
height = 1080

image_1 = numpy.zeros((width, height, 3))
image_2 = numpy.zeros((width, height, 3))
image_3 = numpy.zeros((width, height, 3))

for k in range(255):
    for i in range(width):
        g = (i * 255 / width) 
        for j in range(height):
            b = (j * 255 / height)
            image_1[i,j] = (k, g, b)
            image_2[i,j] = (g, k, b)
            image_3[i,j] = (g, b, k)

    scipy.misc.imsave('all/prueba.png', image_1)
#scipy.misc.imsave('colors_2.png', image_2)
#scipy.misc.imsave('colors_3.png', image_3)

## 256 r 256 b 256 g =
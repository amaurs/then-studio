 import numpy
import scipy
import scipy.misc
from scipy import ndimage
from hilbertcurve.hilbertcurve import HilbertCurve
import imageio


for seed in range(1, 5):
    print("Calculating seed %s" % seed)
    p_1 = seed * 3
    p_2 = seed * 2
    hilbert_curve_plane = HilbertCurve(p_1, 2)
    hilbert_curve_cube = HilbertCurve(p_2, 3)
    
    square_array = []
    cube_array = []
    square_ints = []
    cube_ints = []
    
    
    
    for ii in range(2**(p_2 * 3)):
        square = hilbert_curve_plane.coordinates_from_distance(ii)
        cube = hilbert_curve_cube.coordinates_from_distance(ii)
        
    
        square_int = (square[0] << p_1) | (square[1] << 0)
        cube_int = (cube[0] << (p_2 * 2)) | (cube[1] << p_2) | (cube[2] << 0)
    
        square_ints.append(square_int)
        cube_ints.append(cube_int)
    
        blue = square_int & 0xFF
        green = (square_int & 0xFF00) >> 8
        red = (square_int & 0xFF0000) >> 16
    
        square_array.append([red, green, blue])
        cube_array.append([cube[0]<<(8 - p_2), cube[1]<<(8 - p_2), cube[2]<<(8 - p_2)])
    
        if (ii)%1000==0:
            print(ii/2**(p_2 * 3))
    
    
    image_1 = numpy.zeros((2**p_1, 2**p_1, 3))
    image_2 = numpy.zeros((2**p_1, 2**p_1, 3))
    
    count = 0 
    for x in range(2**p_1):
        for y in range(2**p_1):
            image_1[x, y] = square_array[count]
            image_2[x, y] = cube_array[count]
            count += 1
    
    imageio.imwrite('hilbert_square_%s_%s.png' % (2**p_1, 2**p_1), image_1.astype(numpy.uint8))
    imageio.imwrite('hilbert_cube_%s_%s.png' % (2**p_1, 2**p_1), image_2.astype(numpy.uint8))


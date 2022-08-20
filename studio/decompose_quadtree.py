import numpy
from typing import Tuple
import scipy
import scipy.misc
from scipy import ndimage
import imageio
import numpy as np

size = 2 ** 24
quad_size = len(np.base_repr(size - 1, base=4))
oct_size = len(np.base_repr(size - 1, base=8))

def quad_to_plane(i: int) -> Tuple[int, int]:
    
    quad = np.base_repr(i, base=4).zfill(quad_size)
    x, y = 0, 0
    for i in range(len(quad)):
        position = int(quad[i:i + 1])
        binary = np.base_repr(position, base=2).zfill(2)
        if binary[0] == '1':
            x += 2 ** (len(quad) - i - 1)
        if binary[1] == '1':
            y += 2 ** (len(quad) - i - 1)
    return x, y


def oct_to_space(i: int) -> Tuple[int, int, int]:

    oct_ = np.base_repr(i, base=8).zfill(oct_size)

    x, y, z = 0, 0, 0
    i = 0
    for i in range(len(oct_)):
        position = int(oct_[i:i + 1])
        binary = np.base_repr(position, base=2).zfill(3)
        if binary[0] == '1':
            x += 2 ** (len(oct_) - i - 1)
        if binary[1] == '1':
            y += 2 ** (len(oct_) - i - 1)
        if binary[2] == '1':
            z += 2 ** (len(oct_) - i - 1)
    return x, y, z


if __name__ == '__main__':
    seed = 4
    print("Calculating seed %s" % seed)
    p_1 = seed * 3
    p_2 = seed * 2
    
    square_array = []
    cube_array = []
    square_ints = []
    cube_ints = []
    
    
    
    for ii in range(2**(p_2 * 3)):
        square = quad_to_plane(ii)
        cube = oct_to_space(ii)
        
    
        square_int = (square[0] << p_1) | (square[1] << 0)
        cube_int = (cube[0] << (p_2 * 2)) | (cube[1] << p_2) | (cube[2] << 0)
    
        square_ints.append(square_int)
        cube_ints.append(cube_int)
    
        blue = square_int & 0xFF
        green = (square_int & 0xFF00) >> 8
        red = (square_int & 0xFF0000) >> 16
    
        square_array.append([red, green, blue])
        cube_array.append([cube[0]<<(8 - p_2), cube[1]<<(8 - p_2), cube[2]<<(8 - p_2)])
    
        if (ii)%10000==0:
            print("{:.2f}%".format(100 * ii/2**(p_2 * 3)))
    
    
    image_1 = numpy.zeros((2**p_1, 2**p_1, 3))
    image_2 = numpy.zeros((2**p_1, 2**p_1, 3))
    
    count = 0 
    for x in range(2**p_1):
        for y in range(2**p_1):
            image_1[x, y] = square_array[count]
            image_2[x, y] = cube_array[count]
            count += 1
    
    imageio.imwrite('quadtree_square_%s_%s.png' % (2**p_1, 2**p_1), image_1.astype(numpy.uint8))
    imageio.imwrite('quadtree_cube_%s_%s.png' % (2**p_1, 2**p_1), image_2.astype(numpy.uint8))


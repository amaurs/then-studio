import os
import pathlib
import sys
from typing import Optional

from studio.all_rgb import Decomposer

import imageio
import numpy as np

from studio.all_rgb.flood_fill_decomposer import FloodFillDecomposer
from studio.all_rgb.hilbert_decomposer import HilbertDecomposer
from studio.all_rgb.identity_decomposer import IdentityDecomposer
from studio.all_rgb.quadtree_decomposer import QuadtreeDecomposer


class Composer:

    def __init__(self, plane: Decomposer, space: Decomposer) -> None:
        assert plane.seed == space.seed
        self.plane = plane
        self.space = space

    def create_image(self, directory: Optional[str] = None) -> None:

        p_1 = self.plane.seed * 3
        p_2 = self.space.seed * 2

        square_array = []
        cube_array = []
        square_ints = []
        cube_ints = []
        image_3 = np.zeros((2 ** p_1, 2 ** p_1, 3))

        for ii in range(2 ** (p_2 * 3)):
            square = self.plane.to_plane(ii)
            cube = self.space.to_space(ii)



            square_int = (square[0] << p_1) | (square[1] << 0)
            cube_int = (cube[0] << (p_2 * 2)) | (cube[1] << p_2) | (cube[2] << 0)

            square_ints.append(square_int)
            cube_ints.append(cube_int)

            blue = square_int & 0xFF
            green = (square_int & 0xFF00) >> 8
            red = (square_int & 0xFF0000) >> 16

            square_array.append([red, green, blue])
            cube_array.append([cube[0] << (8 - p_2), cube[1] << (8 - p_2), cube[2] << (8 - p_2)])

            image_3[square[0], square[1]] = [cube[0] << (8 - p_2), cube[1] << (8 - p_2), cube[2] << (8 - p_2)]

            if (ii) % 10000 == 0:
                sys.stdout.write("\r{:.2f}%".format(100 * ii / 2 ** (p_2 * 3)))
                sys.stdout.flush()
        sys.stdout.write("\r{:.2f}%\n".format(100 * ii / 2 ** (p_2 * 3)))
        sys.stdout.flush()
        image_1 = np.zeros((2 ** p_1, 2 ** p_1, 3))
        image_2 = np.zeros((2 ** p_1, 2 ** p_1, 3))

        count = 0
        for x in range(2 ** p_1):
            for y in range(2 ** p_1):
                image_1[x, y] = square_array[count]
                image_2[x, y] = cube_array[count]
                count += 1

        directory = directory or os.path.dirname(os.path.realpath(__file__))

        imageio.imwrite(pathlib.Path(os.path.join(directory, f'{self.plane.name}_square_{2 ** p_1}_{2 ** p_1}.png')), image_1.astype(np.uint8))
        imageio.imwrite(pathlib.Path(os.path.join(directory, f'{self.space.name}_cube_{2 ** p_1}_{2 ** p_1}.png')), image_2.astype(np.uint8))
        imageio.imwrite(pathlib.Path(os.path.join(directory, f'{self.plane.name}_square_{self.space.name}_cube_{2 ** p_1}_{2 ** p_1}.png')), image_3.astype(np.uint8))


if __name__ == '__main__':
    import time
    for i in range(1, 5):
        tic = time.perf_counter()
        Composer(space=QuadtreeDecomposer(seed=i),
                 plane=IdentityDecomposer(seed=i)).create_image()
        toc = time.perf_counter()
        print(f"Total process time: {toc - tic:0.4f} seconds")

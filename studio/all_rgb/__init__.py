import os
import pathlib
import sys
from abc import ABC, abstractmethod
from typing import Tuple, Optional

import imageio
import numpy as np


class Decomposer(ABC):

    def __init__(self, seed: int) -> None:
        self.seed = seed

    @abstractmethod
    def to_space(self, i: int) -> Tuple[int, int, int]:
        ...

    @abstractmethod
    def to_plane(self, i: int) -> Tuple[int, int]:
        ...

    @property
    def name(self) -> str:
        raise NotImplemented("Please implement this for your class.")

    def create_image(self, directory: Optional[str] = None) -> None:

        p_1 = self.seed * 3
        p_2 = self.seed * 2

        square_array = []
        cube_array = []
        square_ints = []
        cube_ints = []

        for ii in range(2 ** (p_2 * 3)):
            square = self.to_plane(ii)
            cube = self.to_space(ii)

            square_int = (square[0] << p_1) | (square[1] << 0)
            cube_int = (cube[0] << (p_2 * 2)) | (cube[1] << p_2) | (cube[2] << 0)

            square_ints.append(square_int)
            cube_ints.append(cube_int)

            blue = square_int & 0xFF
            green = (square_int & 0xFF00) >> 8
            red = (square_int & 0xFF0000) >> 16

            square_array.append([red, green, blue])
            cube_array.append([cube[0] << (8 - p_2), cube[1] << (8 - p_2), cube[2] << (8 - p_2)])

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

        imageio.imwrite(pathlib.Path(os.path.join(directory, f'{self.name}_square_{2 ** p_1}_{2 ** p_1}.png')), image_1.astype(np.uint8))
        imageio.imwrite(pathlib.Path(os.path.join(directory, f'{self.name}_cube_{2 ** p_1}_{2 ** p_1}.png')), image_2.astype(np.uint8))

from typing import Tuple

from studio.all_rgb import Decomposer
import numpy as np

size = 2 ** 24

class QuadtreeDecomposer(Decomposer):

    def __init__(self, seed: int):
        self.seed = seed
        self.quad_size = len(np.base_repr(2 ** (6 * self.seed) - 1, base=4))
        self.oct_size = len(np.base_repr(2 ** (6 * self.seed) - 1, base=8))
    @property
    def name(self) -> str:
        return "quadtree"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return self._oct_to_space(i=i, oct_size=self.oct_size)

    def to_plane(self, i: int) -> Tuple[int, int]:
        return self._quad_to_plane(i=i, quad_size=self.quad_size)

    def _quad_to_plane(self, i: int, quad_size: int) -> Tuple[int, int]:
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

    def _oct_to_space(self, i: int, oct_size: int) -> Tuple[int, int, int]:
        oct_ = np.base_repr(i, base=8).zfill(oct_size)
        x, y, z = 0, 0, 0
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

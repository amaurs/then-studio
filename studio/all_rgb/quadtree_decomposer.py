from typing import Tuple

from studio.all_rgb import Decomposer
import numpy as np

size = 2 ** 24

quad_size = len(np.base_repr(size - 1, base=4))
oct_size = len(np.base_repr(size - 1, base=8))


class QuadtreeDecomposer(Decomposer):

    @property
    def name(self) -> str:
        return "quadtree"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return self._oct_to_space(i=i)

    def to_plane(self, i: int) -> Tuple[int, int]:
        return self._quad_to_plane(i=i)

    def _quad_to_plane(self, i: int) -> Tuple[int, int]:
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

    def _oct_to_space(self, i: int) -> Tuple[int, int, int]:
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


if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    QuadtreeDecomposer(seed=4).create_image()
    toc = time.perf_counter()
    print(f"Total process time: {toc - tic:0.4f} seconds")


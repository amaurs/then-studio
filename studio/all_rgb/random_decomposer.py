import random
from typing import Tuple

from studio.all_rgb import Decomposer


class RandomDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        super().__init__(seed=seed)

        plane_size = 2 ** (self.seed * 3)
        space_size = 2 ** (self.seed * 2)

        plane = []
        space = []

        for x in range(plane_size):
            for y in range(plane_size):
                plane.append((x, y))

        for x in range(space_size):
            for y in range(space_size):
                for z in range(space_size):
                    space.append((x, y, z))

        random.shuffle(plane)
        random.shuffle(space)

        self.space = space

    @property
    def name(self) -> str:
        return "random"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return self.space[i]

    def to_plane(self, i: int) -> Tuple[int, int]:
        x = i & (2 ** (self.seed * 3) - 1)
        y = (i >> (self.seed * 3)) & (2 ** (self.seed * 3) - 1)
        return x, y


if __name__ == '__main__':
    RandomDecomposer(seed=2)

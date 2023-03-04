import random
from functools import lru_cache
from typing import Tuple, List

from studio.all_rgb import Decomposer

import numpy as np


class SimulatedAnnealingDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        super().__init__(seed=seed)
        self.oct_size = len(np.base_repr(2 ** (6 * self.seed) - 1, base=8))
        space_size = 2 ** (self.seed * 2)
        # asign each color to its own index
        space = [np.base_repr(i, base=8).zfill(self.oct_size) for i in range(space_size ** 3)]
        # and now shuffle them
        random.shuffle(space)

        for _ in range(1000):

            i = random.randint(0, len(space) - 1)
            color_a = space[i]
            neighbors_a = SimulatedAnnealingDecomposer.get_neighbors(
                index=i,
                directions=((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1),
                                (2, 0), (2, -2), (0, -2), (-2, -2), (-2, 0), (-2, 2), (0, 2), (2, 2),
                                (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)),
                width=space_size,
                height=space_size)

            distance_a_orig = SimulatedAnnealingDecomposer.proxy(main=color_a, colors=[space[k] for k in neighbors_a])

            tries = 0
            while True:
                tries += 1
                if _ % 100000 == 0:
                    print(f"{_}:{tries}")
                j = random.randint(0, len(space) - 1)
                color_b = space[j]
                neighbors_b = SimulatedAnnealingDecomposer.get_neighbors(
                    index=j,
                    directions=((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1),
                                (2, 0), (2, -2), (0, -2), (-2, -2), (-2, 0), (-2, 2), (0, 2), (2, 2),
                                (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)),
                    width=space_size,
                    height=space_size)
                distance_b_orig = SimulatedAnnealingDecomposer.proxy(main=color_b,
                                                                     colors=[space[k] for k in neighbors_b])
                distance_orig = distance_a_orig + distance_b_orig
                distance_a_in_b_neighborhood = SimulatedAnnealingDecomposer.proxy(
                    main=color_a,
                    colors=[space[k] for k in neighbors_b])
                distance_b_in_a_neighborhood = SimulatedAnnealingDecomposer.proxy(
                    main=color_b,
                    colors=[space[k] for k in neighbors_a])
                distance_new = distance_a_in_b_neighborhood + distance_b_in_a_neighborhood

                if distance_new > distance_orig or tries > 25:
                    space[i], space[j] = space[j], space[i]
                    break

        self.space = space

    @property
    def name(self) -> str:
        return "simulated_annealing"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        oct_ = self.space[i]
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

    def to_plane(self, i: int) -> Tuple[int, int]:
        # 12, 9, 6, 3
        x = i & (2 ** (self.seed * 3) - 1)
        y = (i >> (self.seed * 3)) & (2 ** (self.seed * 3) - 1)
        return x, y

    @staticmethod
    def proxy(main: str, colors: List[str]) -> int:
        total = 0
        for color in colors:
            for i in range(len(main)):
                if main[i] == color[i]:
                    total += 1
                else:
                    break
        return total

    @staticmethod
    def index_to_xy(index: int, width: int, height: int) -> Tuple[int, int]:
        return index % width, index // height

    @staticmethod
    def xy_to_index(x: int, y: int, height: int) -> int:
        return y * height + x

    @staticmethod
    @lru_cache(maxsize=None)
    def get_neighbors(index: int, directions: Tuple[Tuple[int, int], ...], width: int, height: int) -> List[int]:
        x0, y0 = SimulatedAnnealingDecomposer.index_to_xy(index=index, width=width, height=height)
        return [SimulatedAnnealingDecomposer.xy_to_index(x=(x0 + x) % width, y=(y0 + y) % height, height=height) for x, y in directions]


if __name__ == '__main__':
    q = SimulatedAnnealingDecomposer(seed=2)

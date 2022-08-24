from typing import Tuple

from studio.all_rgb import Decomposer


class IdentityDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        self.seed = seed

    @property
    def name(self) -> str:
        return "identity"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        # 24, 18, 12, 6
        blue = i & (2 ** (self.seed * 2) - 1)
        green = (i >> (self.seed * 2)) & (2 ** (self.seed * 2) - 1)
        red = (i >> (self.seed * 2 * 2)) & (2 ** (self.seed * 2) - 1)
        return red, green, blue
    def to_plane(self, i: int) -> Tuple[int, int]:
        # 12, 9, 6, 3
        x = i & (2 ** (self.seed * 3) - 1)
        y = (i >> (self.seed * 3)) & (2 ** (self.seed * 3) - 1)
        return x, y

if __name__ == '__main__':
    import time
    for i in range(1, 5):
        tic = time.perf_counter()
        decomposer = IdentityDecomposer(seed=i).create_image()
        toc = time.perf_counter()
        print(f"Total process time: {toc - tic:0.4f} seconds")

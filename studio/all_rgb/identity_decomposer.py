from typing import Tuple

from studio.all_rgb import Decomposer


class IdentityDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        self.seed = seed

    @property
    def name(self) -> str:
        return "identity"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        blue = i & 255
        green = (i >> 8) & 255
        red = (i >> 16) & 255
        return red, green, blue
    def to_plane(self, i: int) -> Tuple[int, int]:
        x = (i >> 12) & 4095
        y = i & 4095
        return x, y

if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    decomposer = IdentityDecomposer(seed=4).create_image()
    toc = time.perf_counter()
    print(f"Total process time: {toc - tic:0.4f} seconds")

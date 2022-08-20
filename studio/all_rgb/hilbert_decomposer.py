from typing import Tuple

from hilbertcurve.hilbertcurve import HilbertCurve

from studio.all_rgb import Decomposer


class HilbertDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self.hilbert_curve_plane = HilbertCurve(self.seed * 3, 2)
        self.hilbert_curve_cube = HilbertCurve(self.seed * 2, 3)

    @property
    def name(self) -> str:
        return "hilbert"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return self.hilbert_curve_cube.point_from_distance(distance=i)

    def to_plane(self, i: int) -> Tuple[int, int]:
        return self.hilbert_curve_plane.point_from_distance(distance=i)


if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    HilbertDecomposer(seed=4).create_image()
    toc = time.perf_counter()
    print(f"Total process time: {toc - tic:0.4f} seconds")

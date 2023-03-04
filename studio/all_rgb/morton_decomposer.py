from typing import Tuple

from studio.all_rgb import Decomposer
import zCurve as z


class MortonDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        self.seed = seed

    @property
    def name(self) -> str:
        return "morton"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return tuple(z.deinterlace(code_point=i, dims=3))

    def to_plane(self, i: int) -> Tuple[int, int]:
        return tuple(z.deinterlace(code_point=i, dims=2))

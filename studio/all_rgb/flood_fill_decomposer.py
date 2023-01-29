import random
from collections import deque
from typing import Tuple, List, Set, cast
from functools import lru_cache
from studio.all_rgb import Decomposer


class FloodFillDecomposer(Decomposer):

    def __init__(self, seed: int) -> None:
        super().__init__(seed=seed)

        self._plane_walk: Tuple[int, int] = cast(Tuple[int, int], self.floodfill(
            dimension=2,
            directions=[(1, 0), (0, 1), (-1, 0), (0, -1)],
            size=2 ** (seed * 3)))
        self._space_walk: Tuple[int, int, int] = cast(Tuple[int, int, int], self.floodfill(
            dimension=3,
            directions=[(0, 0, 1), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)],
            size=2 ** (seed * 2)))

    @property
    def name(self) -> str:
        return "flood_fill"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        return self._space_walk[i]

    def to_plane(self, i: int) -> Tuple[int, int]:
        return self._plane_walk[i]

    @staticmethod
    @lru_cache(maxsize=None)
    def _is_out_of_bounds(point: Tuple[int, ...], size: int) -> bool:
        return any(entry < 0 or size - 1 < entry for entry in point)

    @staticmethod
    def _get_neighbors(point: Tuple[int, ...], directions: List[Tuple[int, ...]], seen: Set[Tuple[int, ...]],
                       size: int) -> List[Tuple[int, ...]]:
        neighbors = []
        for direction in directions:
            neighbor = tuple(sum(x) for x in zip(point, direction))
            if not FloodFillDecomposer._is_out_of_bounds(neighbor, size=size) and neighbor not in seen:
                neighbors.append(neighbor)
                seen.add(neighbor)
        return neighbors

    @staticmethod
    def floodfill(dimension: int, directions: List[Tuple[int, ...]], size: int) -> List[Tuple[int, ...]]:
        origin = tuple(int(size / 2) for _ in range(dimension))
        queue = deque([origin])
        seen = {origin}
        visited = []
        i = 0
        while len(queue):
            i += 1
            point = queue.popleft()
            visited.append(point)
            for neighbor in FloodFillDecomposer._get_neighbors(
                    point=point,
                    directions=directions,
                    size=size,
                    seen=seen):
                queue.append(neighbor)
            if i % 10000 == 0:
                print(100.0 * len(visited) / (size ** dimension))
        return visited

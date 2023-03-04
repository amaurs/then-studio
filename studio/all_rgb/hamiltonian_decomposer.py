import random
from typing import Tuple
import igraph as ig
from studio.all_rgb import Decomposer


class HamiltonianDecomposer(Decomposer):

    def __init__(self, seed: int, weight_randomness=10) -> None:
        super().__init__(seed=seed)
        self.weight_randomness = weight_randomness
        plane_size = 2 ** (self.seed * 3)
        cube_size = 2 ** (self.seed * 2)

        plane_lattice = ig.Graph.Lattice([plane_size, plane_size], circular=False)
        cube_lattice = ig.Graph.Lattice([cube_size, cube_size, cube_size], circular=False)

        plane_weights = [random.randint(1, weight_randomness) for _ in plane_lattice.es]
        cube_weights = [random.randint(1, weight_randomness) for _ in cube_lattice.es]

        self.plane_spanning_tree = plane_lattice.spanning_tree(plane_weights, return_tree=True)
        self.cube_spanning_tree = cube_lattice.spanning_tree(cube_weights, return_tree=True)

        self.plane_vertex_dfs = self.plane_spanning_tree.dfs(int(len(cube_lattice.vs) / 2))[0]
        self.cube_vertex_dfs = self.cube_spanning_tree.dfs(int(len(cube_lattice.vs) / 2))[0]

        self.layout_2d = plane_lattice.layout("grid")
        self.layout_3d = cube_lattice.layout("grid_3d")

    @property
    def name(self) -> str:
        return f"hamiltonian_weight_randomness_{self.weight_randomness}"

    def to_space(self, i: int) -> Tuple[int, int, int]:
        r, g, b = self.layout_3d[self.cube_vertex_dfs[i]]
        return int(r), int(g), int(b)

    def to_plane(self, i: int) -> Tuple[int, int]:
        x, y = self.layout_2d[self.plane_vertex_dfs[i]]
        return int(x), int(y)


if __name__ == '__main__':
    HamiltonianDecomposer(seed=3, weight_randomness=729)

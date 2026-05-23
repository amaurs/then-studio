#!/usr/bin/env python3
# Usage: python generate.py <plane> [space] [--seed 1-4] [--output DIR]
# Example: python generate.py hilbert random --seed 3 --output output
import argparse
import os

from studio.all_rgb.composer import Composer
from studio.all_rgb.flood_fill_decomposer import FloodFillDecomposer
from studio.all_rgb.hamiltonian_decomposer import HamiltonianDecomposer
from studio.all_rgb.hilbert_decomposer import HilbertDecomposer
from studio.all_rgb.identity_decomposer import IdentityDecomposer
from studio.all_rgb.morton_decomposer import MortonDecomposer
from studio.all_rgb.quadtree_decomposer import QuadtreeDecomposer
from studio.all_rgb.random_decomposer import RandomDecomposer
from studio.all_rgb.simulated_annealing_decomposer import SimulatedAnnealingDecomposer

ALGORITHMS = {
    "flood-fill": FloodFillDecomposer,
    "hamiltonian-cycle": HamiltonianDecomposer,
    "hilbert": HilbertDecomposer,
    "identity": IdentityDecomposer,
    "morton": MortonDecomposer,
    "quadtree": QuadtreeDecomposer,
    "random": RandomDecomposer,
    "simulated-annealing": SimulatedAnnealingDecomposer,
}

def main():
    parser = argparse.ArgumentParser(
        description="Generate all-RGB color decomposition images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  python generate.py hilbert
  python generate.py hilbert random          # hilbert layout, random colors
  python generate.py identity hilbert --seed 2
"""
    )
    parser.add_argument("plane", choices=ALGORITHMS.keys(), help="Algorithm for pixel layout (plane decomposer)")
    parser.add_argument("space", choices=ALGORITHMS.keys(), nargs="?", help="Algorithm for color assignment (space decomposer); defaults to plane")
    parser.add_argument("--seed", type=int, default=3, help="Seed controls resolution: 1=8px, 2=64px, 3=512px, 4=4096px (default: 3)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    plane = ALGORITHMS[args.plane](seed=args.seed)
    space = ALGORITHMS[args.space](seed=args.seed) if args.space else plane

    Composer(plane=plane, space=space).create_image(directory=args.output)

    res = 2 ** (args.seed * 3)
    print(f"Written to {args.output}/:")
    print(f"  {plane.name}_square_{res}_{res}.png")
    print(f"  {space.name}_cube_{res}_{res}.png")
    if plane is not space:
        print(f"  {plane.name}_square_{space.name}_cube_{res}_{res}.png")

if __name__ == "__main__":
    main()

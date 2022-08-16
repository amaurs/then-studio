from typing import Tuple
import numpy as np
from PIL import Image


def quad_to_plane(quad: str) -> Tuple[int, int]:
    x, y = 0, 0
    for i in range(len(quad)):
        position = int(quad[i:i + 1])
        binary = np.base_repr(position, base=2).zfill(2)
        if binary[0] == '1':
            x += 2 ** (len(quad) - i - 1)
        if binary[1] == '1':
            y += 2 ** (len(quad) - i - 1)
    return x, y


def oct_to_space(oct_: str) -> Tuple[int, int, int]:
    x, y, z = 0, 0, 0
    i = 0
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


if __name__ == "__main__":
    size = 2 ** 24
    data = np.zeros((2 ** 12, 2 ** 12, 3), dtype=np.uint8)
    quad_size = len(np.base_repr(size - 1, base=4))
    oct_size = len(np.base_repr(size - 1, base=8))
    print(oct_to_space(oct_=np.base_repr(size - 1, base=8).zfill(oct_size)))
    print(quad_to_plane(quad=np.base_repr(size - 1, base=4).zfill(quad_size)))
    for i in range(size):
        x, y = quad_to_plane(quad=np.base_repr(i, base=4).zfill(quad_size))
        r, g, b = oct_to_space(oct_=np.base_repr(i, base=8).zfill(oct_size))
        data[x, y] = [r, g, b]
        if i % 100000 == 0:
            print(f"{i}:[{x}, {y}] = ({r}, {g}, {b})")
    img = Image.fromarray(data, 'RGB')
    img.save('quad_tree.png')

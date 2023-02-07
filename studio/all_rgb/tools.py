import concurrent.futures
import os
import pathlib
import sys
import time
from itertools import product
from typing import Any

import imageio
import numpy as np


def process(image: Any, r_origin: int, b_origin: int, g_origin: int, threshold: int) -> None:
    directory = f"output"
    output = np.full(image.shape, (255, 255, 255))
    width, height, _ = image.shape

    for i, (x, y) in enumerate(product(range(width), range(height))):
        r, g, b = image[x, y]
        if r_origin <= r < r_origin + threshold and b_origin <= b < b_origin + threshold and g_origin <= g < g_origin + threshold:
            output[x, y] = image[x, y]
        if i % 10000 == 0:
            sys.stdout.write("\r{:.2f}%".format(100 * i / (width * height)))
            sys.stdout.flush()
    sys.stdout.write("\r{:.2f}%\n".format(100 * i / (width * height)))
    sys.stdout.flush()
    imageio.imwrite(
        pathlib.Path(os.path.join(directory, f"hamiltonian-1-{threshold}-{(r_origin, g_origin, b_origin)}.png")),
        output.astype(np.uint8))


if __name__ == '__main__':
    image = imageio.imread("output/hamiltonian-1.png")  # this image came from https://allrgb.com/hamiltonian-1
    tic = time.perf_counter()
    futures = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for threshold in [128]:
            for i, (r_origin, g_origin, b_origin) in enumerate(product(range(0, 256, threshold), range(0, 256, threshold), range(0, 256, threshold))):
                print(f"{i}:{threshold}:{(r_origin, g_origin, b_origin)}")
                futures[(threshold, r_origin, g_origin, b_origin)] = executor.submit(process, image, r_origin, b_origin, g_origin, threshold)

    for key, future in futures.items():
        print(key)
        future.result()

    toc = time.perf_counter()
    print(f"Total process time: {toc - tic:0.4f} seconds")
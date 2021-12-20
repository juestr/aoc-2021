#!/usr/bin/env python3

import sys
import numpy as np
from scipy import ndimage


def run(img, n=1, pad=None, callback=None):
    kernel = 1 << np.arange(9).reshape(3, 3)
    padded = np.pad(img, pad or n)
    for i in range(n):
        indices = ndimage.convolve(padded, kernel)
        padded = algo[indices]
        callback and callback(i, padded)
    return padded

def show(i, img):
    np.set_printoptions(linewidth=1_000, threshold=1_000_000, formatter={'int': ' #'.__getitem__})
    print('-' * 25, i, '-' * 25)
    print(img)
    np.set_printoptions()


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc20_game_of_life.txt') as f:
        input = f.read().splitlines()

    algo = np.array([bit == '#' for bit in input[0]], dtype=np.int16)
    img = np.array([[bit == '#' for bit in row] for row in input[2:]], dtype=np.int16)
    run(img, *map(int, sys.argv[2:4]), callback=show)

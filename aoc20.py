#!/usr/bin/env python3

import sys
import numpy as np
from scipy import ndimage

with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc20_input.txt') as f:
    input = f.read().splitlines()


def enhance(img, n):
    kernel = 1 << np.arange(9).reshape(3, 3)
    padded = np.pad(img, n)
    for _ in range(n):
        indices = ndimage.convolve(padded, kernel)
        padded = algo[indices]
    return padded

algo = np.array([bit == '#' for bit in input[0]], dtype=np.int16)
img = np.array([[bit == '#' for bit in row] for row in input[2:]], dtype=np.int16)
lit = np.sum(enhance(img, 2))

print(f'Part 1: {lit=}')


lit = np.sum(enhance(img, 50))

print(f'Part 2: {lit=}')

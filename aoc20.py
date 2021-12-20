#!/usr/bin/env python3

import numpy as np
from scipy import ndimage

# with open('aoc20_example.txt') as f:
with open('aoc20_input.txt') as f:
    a20 = f.read().splitlines()


algo = np.array([bit == '#' for bit in a20[0]], dtype=np.int16)
img = np.array([[bit == '#' for bit in row] for row in a20[2:]], dtype=np.int16)

def enhance(img, n):
    kernel = 1 << np.arange(9).reshape(3, 3)
    padded = np.pad(img, n)
    for _ in range(n):
        indices = ndimage.convolve(padded, kernel)
        padded = algo[indices]
    return padded

lit = np.sum(enhance(img, 2))

print(f'Part 1: {lit=}')


lit = np.sum(enhance(img, 50))

print(f'Part 2: {lit=}')

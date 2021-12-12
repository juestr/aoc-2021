#!/usr/bin/env python3

import numpy as np
from scipy.ndimage import correlate


with open('aoc11_input.txt') as f:
    a = np.genfromtxt(f, delimiter=1, dtype=np.int_)


NBKERNEL = np.array(
    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]])

def step(a):
    a += 1

    active = np.ones_like(a, dtype=np.bool_)
    while np.any(new_flashes:=(a > 9) & active):
        nb_increases = correlate(new_flashes.astype(np.int_), NBKERNEL,
            mode='constant', cval=False) * active
        a += nb_increases
        active &= ~new_flashes

    a *= active
    return a.size - np.sum(active)

flashes = sum(step(a) for _ in range(100))
print(f'Part 1: {flashes=}')


at_step = 101
while step(a) != a.size:
    at_step += 1

print(f'Part 2: {at_step=}')

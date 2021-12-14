#!/usr/bin/env python3

from functools import reduce
import re
import numpy as np

with open('aoc13_input.txt') as f:
    a13 = f.read().splitlines()


xs, ys, ds = ([int(m.group(1)) for l in a13 if (m:=re.search(p, l))]
    for p in (r'(\d+),', r',(\d+)', r'=(\d+)'))
axes = [m.group(1) == 'x' for l in a13 if (m:=re.search(r'([xy])=', l))]

dots = np.empty((max(ys) + 1, max(xs) + 1), dtype=np.int8)
dots[(ys, xs)] = True

def fold(dots, crease):
    # note: mutates dots and returns a new view on it
    axis, d = crease
    if axis:
        return fold(dots.T, (False, d)).T
    elif d < (l:=dots.shape[0]) // 2:
        # apparently unused, are creases always beyond half?
        return fold(dots[::-1], (False, l - d - 1))[::-1]
    else:
        dots[2*d + 1 - l:d] |= dots[l:d:-1]
        return dots[:d]

dots1 = fold(dots.copy(), (axes[0], ds[0]))
n = np.sum(dots1)

print(f'Part 1: {n=} {dots1.shape=}')


dots2 = reduce(fold, zip(axes, ds), dots.copy())

np.set_printoptions(linewidth=100, formatter={'int': ' #'.__getitem__})
print(f'Part 2: {dots2.shape=}')
print(dots2)  # ascii art result

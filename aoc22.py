#!/usr/bin/env python3

from itertools import chain, product
import re
import sys
import numpy as np


with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc22_input.txt') as f:
    input = f.read().splitlines()
pattern = r'((?:on)|(?:off)) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
steps = [(groups[0] == 'on', tuple(map(int, groups[1:])))
    for line in input for groups in (re.fullmatch(pattern, line).groups(),)]


init_area = np.zeros((101, 101, 101), dtype=np.int8)
for onoff, volume in steps:
    x1, x2, y1, y2, z1, z2 = np.add(volume, 50)
    init_area[x1:x2+1, y1:y2+1, z1:z2+1] = onoff
on = np.sum(init_area)

print(f'Part 1: {on=}')


def partition1d(base, line):
    """Return segments of line inside and outside base"""

    (b1, b2), (l1, l2) = base, line
    if l2 <= b1 or b2 <= l1:
        return (), (line,)
    elif b1 <= l1 and l2 <= b2:
        return (line,), ()
    else:
        left = ((l1, b1),) if l1 < b1 else ()
        right = ((b2, l2),) if b2 < l2 else ()
        return ((max(l1, b1), min(l2, b2)),), left + right

def partition3d(base, volume):
    """Return cuboid parts of volume inside and outside base

    Note: This splits orthogonally into 1-27 pieces, which isn't optimal
    but simple.
    """

    bx1, bx2, by1, by2, bz1, bz2 = base
    x1, x2, y1, y2, z1, z2 = volume
    xinside, xoutside = partition1d((bx1, bx2), (x1, x2))
    yinside, youtside = partition1d((by1, by2), (y1, y2))
    zinside, zoutside = partition1d((bz1, bz2), (z1, z2))
    vs = tuple(tuple(chain.from_iterable(p))
        for p in product(xinside+xoutside, yinside+youtside, zinside+zoutside))
    if all((xinside, yinside, zinside)):
        return vs[:1], vs[1:]
    else:
        return (), vs

def addv(universe, volume):
    additions = [volume]
    for base in universe:
        for v in additions[:]:
            inside, outside = partition3d(base, v)
            if inside:
                additions.remove(v)
                additions.extend(outside)
    universe.extend(additions)

def removev(universe, volume):
    for base in universe[:]:
        inside, outside = partition3d(volume, base)
        if inside:
            universe.remove(base)
            universe.extend(outside)

universe = []
for onoff, (x1, x2, y1, y2, z1, z2) in steps:
    (removev, addv)[onoff](universe, (x1, x2+1, y1, y2+1, z1, z2+1))
on = sum((x2-x1) * (y2-y1) * (z2-z1) for x1, x2, y1, y2, z1, z2 in universe)

print(f'Part 2: {on=}')

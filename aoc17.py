#!/usr/bin/env python3

from itertools import repeat
from math import ceil, floor
import re

with open('aoc17_input.txt') as f:
    a17 = f.read()

pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
x1, x2, y1, y2 = map(int, pattern.match(a17).groups())
# print('target x=', x1, x2, 'y=', y1, y2)

def sumn(n):
    return n * (n + 1) // 2

def distx(vx0, t):
    return sumn(vx0) - sumn(max(vx0 - t, 0))

def disty(vy0, t):
    return vy0 * t - sumn(t-1)

def maxheight(vy0, t):
    tmax = min(vy0, t)
    return 0 if vy0 <= 0 else vy0 * tmax - sumn(tmax - 1)

# limits only, not guaranteed to fall into target area after rounding
def min_vy0(t):
    return ceil(t/2 - 1/2 + y1/t)
def max_vy0(t):
    return floor(t/2 - 1/2 + y2/t)

# vy0_min(t) = t/2 - 1/2 + y1/t
# vy0_max(t) = t/2 - 1/2 + y2/t
# For t >= t_limit it can be seen both bounds fall into (C+e, C+1/2-e)
# for a 2C in N, a small 0<e<0.5 and y1, y2 not of opposite signs,
# so no integer solution is possible.
assert y1 * y2 >= 0, 'infinite solutions'
t_limit = max(abs(y1), abs(y2)) * 2 + 1

# brute forcing this is easier than all analytical corner cases
highest_y = max(maxheight(vy0, t)
    for vx0 in range(min(x1, 0), max(x2+1, 1))
    for t in range(1, t_limit)
    if x1 <= distx(vx0, t) <= x2
    if y1 <= disty((vy0:=max_vy0(t)), t) <= y2)

print(f'Part 1: {highest_y=}')


number = len({(vx0, vy0)
    for vx0 in range(1, x2+1)
    for t in range(1, t_limit)
    if x1 <= distx(vx0, t) <= x2
    for vy0 in range(min_vy0(t), max_vy0(t)+1)})

print(f'Part 2: {number=}')

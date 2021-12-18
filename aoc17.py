#!/usr/bin/env python3

from itertools import repeat
from math import ceil, floor
import re

with open('aoc17_input.txt') as f:
    a17 = f.read()

pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
x1, x2, y1, y2 = map(int, pattern.match(a17).groups())
print('target x=', x1, x2, 'y=', y1, y2)
assert 0 <= x1 <= x2

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

vx0_t = [(vx0, t)
    for vx0 in range(1, x2+1)
    for t in range(1, vx0+1)  # for now no zero x movements
    if x1 <= (x:=distx(vx0, t)) <= x2]

# vy0_min = t/2 + 1/2 + y1/t
# vy0_max = t/2 + 1/2 + y2/t
# no integer solution for vy0 in [vy0_min, vy0_max] beyond magic_limit?
magic_limit = 1000  # ~ abs(y1) * abs(y2) ?
for vx0, t in vx0_t[:]:
    if vx0 == t:
        # at t vx is zero and we are in target area
        vx0_t += list(zip(repeat(vx0), range(t + 1, magic_limit)))
        # could `break` here but for part 2

highest_y = max(maxheight(vy0, t)
    for _, t in vx0_t if y1 <= disty((vy0:=max_vy0(t)), t) <= y2)

print(f'Part 1: {highest_y=}')


number = len({(vx0, vy0)
    for vx0, t in vx0_t
    for vy0 in range(min_vy0(t), max_vy0(t)+1)})

print(f'Part 2: {number=}')
